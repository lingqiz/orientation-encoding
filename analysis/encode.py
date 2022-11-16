import torch, math, einops, numpy as np
from torch.distributions import MultivariateNormal
from torch.autograd.functional import jacobian
from astropy.stats import circstats
from scipy.optimize import minimize, Bounds
from warnings import warn

class VoxelEncodeBase():
    '''
    Base class for Voxel Encoding Models
    '''

    @staticmethod
    def tuning(stim, pref):
        '''
        Orientation (basis) tuning function
        '''
        stim = einops.repeat(stim, 'n -> n k', k = pref.shape[0])
        nonlinr = torch.cos(math.pi * (stim - pref) / 90.0)
        rectify = torch.maximum(torch.zeros_like(nonlinr), nonlinr)
        resp = torch.pow(rectify, 5)

        return resp

    @staticmethod
    def circ_mean(value, prob):
        '''
        Compute the mean of a circular probability distribution
        '''
        mean = circstats.circmean(value / 90.0 * math.pi, weights=prob)

        # convert to [0, 2 * pi] ard range
        if mean < 0:
            mean += math.pi * 2

        # convert to [0, 180] deg range
        return mean / math.pi * 90.0

    @staticmethod
    def circ_std(value, prob):
        '''
        Compute the standard deviation of a circular probability distribution
        '''
        std = circstats.circstd(value / 90.0 * math.pi, weights=prob)
        return std / math.pi * 90.0

    def __init__(self, n_func=8, device='cpu'):
        '''
        n_func: number of basis functions
        '''
        self.pref = torch.arange(0, 180.0, 180.0 / n_func, dtype=torch.float32, device=device)
        self.device = device
        self.beta = None

    def forward(self, stim):
        '''
        Predict voxel responses given stimulus value
        '''
        if self.beta is None:
            raise Exception("Model weights are not yet estimated")

        stim = torch.tensor(stim, dtype=torch.float32, device=self.device)
        resp = self.tuning(stim, self.pref)
        return (resp @ self.beta).t()

    def derivative(self, delta=1.0):
        '''
        Compute the derivative of the tuning function
        '''
        domain = torch.arange(0, 180, delta, dtype=torch.float32, device=self.device)
        forward = lambda x: self.tuning(x, self.pref) @ self.beta

        # take the derivative of the tuning function at each stimulus value
        result = []
        for stim in domain:
            diff = jacobian(forward, torch.tensor([stim], device=self.device))
            result.append(diff.squeeze().unsqueeze(1))

        return torch.cat(result, dim=1)

    def ols(self, stim, voxel):
        '''
        Estimate model weights given stimulus and response
        Stage 1: estimate beta weights using least-square

        stim: stimulus value (n_trial)
        voxel: voxel responses of shape (n_voxel, n_trial)
        '''
        stim = torch.tensor(stim, dtype=torch.float32, device=self.device)
        voxel = torch.tensor(voxel, dtype=torch.float32, device=self.device)

        rgs = self.tuning(stim, self.pref)
        self.beta = torch.linalg.solve(rgs.t() @ rgs, rgs.t() @ voxel.t())

        return self.beta

class VoxelEncodeNoise(VoxelEncodeBase):

    def __init__(self, n_func=8, device='cpu'):
        '''
        n_func: number of basis functions
        rho: global noise correlation between voxels
        sigma: vector of noise standard deviations
        '''
        super().__init__(n_func, device)
        self.rho = 0.0
        self.sigma = None
        self.cov = None

    def forward(self, stim):
        '''
        Sample from a multivariate normal distribution model of voxel responses
        '''
        # mean response through tuning function
        mean_resp = super().forward(stim)
        sample = torch.zeros_like(mean_resp, device=self.device)

        # sample from multivariate normal distribution
        for idx in range(mean_resp.shape[1]):
            dist = MultivariateNormal(mean_resp[:, idx], self.cov)
            sample[:, idx] = dist.sample()

        return sample

    def fisher(self, delta=1.0):
        '''
        Fisher information as a function of stimulus
        '''
        fprime = self.derivative(delta)
        fisher = fprime.t() @ torch.inverse(self.cov) @ fprime
        return torch.diag(fisher)

    # orientation decoding
    def decode(self, voxel, method='mle'):
        '''
        Compute the likelihood and estimate
        of orientation given voxel activities
        '''
        delta = 0.5
        ornt = np.arange(0, 180.0, delta, dtype=np.float32)
        voxel = einops.repeat(voxel, 'n -> n k', k = ornt.shape[0])

        log_llhd = - self.objective(ornt, voxel, self.cov, sum_llhd=False)

        if method == 'mle':
            estimate = ornt[torch.argmax(log_llhd)]
            return estimate, log_llhd

        elif method == 'mean':
            prob = torch.exp(log_llhd - torch.max(log_llhd))
            prob = (prob / torch.sum(prob)).cpu().numpy()

            est = self.circ_mean(ornt, prob)
            std = self.circ_std(ornt, prob)
            return est, std, prob

        elif method == 'llhd':
            return log_llhd

    # multivariate normal distribution negative log-likelihood
    def _log_llhd(self, x, mu, logdet, invcov):
        return logdet + torch.diag((x - mu).t() @ invcov @ (x - mu))

    # objective function for mle fitting and orientation decoding
    def objective(self, stim, voxel, cov, sum_llhd=True):
        voxel = torch.tensor(voxel, dtype=torch.float32, device=self.device)
        mean_resp = super().forward(stim)

        # log-det of the covariance matrix and its inverse
        logdet = torch.logdet(cov)
        invcov = torch.inverse(cov)

        # compute negative log-likelihood
        vals = self._log_llhd(voxel, mean_resp, logdet, invcov)

        if not sum_llhd:
            return vals

        return torch.sum(vals) / voxel.shape[1]

    # define the covariance matrix (noise model)
    def _cov_mtx(self, rho, sigma):
        return (1 - rho) * torch.diag((sigma ** 2).flatten()) + rho * (sigma @ sigma.t())

    def _clamp(self, rho, sigma):
        '''
        Range constraint
        '''
        with torch.no_grad():
            rho.clamp_(0.0, 1.0 - 1e-6)
            sigma.clamp_min_(1e-6)

    def _mle(self, para, stim, voxel, lr, n_iter, n_print):
        '''
        Estimate model weights given stimulus and response
        Stage 2: estimate noise covariance matrix using maximum likelihood

        stim: stimulus value (n_trial)
        voxel: voxel responses of shape (n_voxel, n_trial)
        '''
        optim = torch.optim.Adam(para, lr=lr)

        # run optimization
        for iter in range(n_iter):
            optim.zero_grad()

            # compute the negative log-likelihood
            cov = self._cov_mtx(*para)
            loss = self.objective(stim, voxel, cov)

            # run the optimization step
            loss.backward()
            optim.step()

            # range constraint
            self._clamp(*para)

            # print loss
            if iter % n_print == 0:
                print("Iter: {}, NegLL: {}".format(iter, loss.item()))
        return

    # estimate noise model
    def mle(self, stim, voxel, lr=0.025, n_iter=250, n_print=50):
        '''
        Wrapper for maximum likelihood estimation
        '''
        # initialize noise model parameters
        rho = torch.zeros(1, dtype=torch.float32, requires_grad=True, device=self.device)
        sigma = torch.ones(voxel.shape[0], dtype=torch.float32, requires_grad=True, device=self.device)

        # run mle using gradient descent
        self._mle([rho, sigma], stim, voxel, lr, n_iter, n_print)

        # save noise model parameters
        self.rho = rho.item()
        self.sigma = sigma.detach().clone()
        self.cov = self._cov_mtx(self.rho, self.sigma)

        return self.rho, self.sigma.clone()

class VoxelEncode(VoxelEncodeNoise):

    def __init__(self, n_func=8, device='cpu'):
        super().__init__(n_func, device=device)

        # additional channel noise parameter
        self.chnl = None

    # override (full) noise model
    def _cov_mtx(self, rho, sigma, chnl):
        return rho * (sigma @ sigma.t()) \
        + (1 - rho) * torch.diag((sigma ** 2).flatten()) \
        + (chnl ** 2) * self.beta.t() @ self.beta

    # range constraint for the model parameters
    def _clamp(self, rho, sigma, chnl):
        '''
        Range constraint
        '''
        with torch.no_grad():
            rho.clamp_(0.0, 1.0 - 1e-6)
            sigma.clamp_min_(1e-6)
            chnl.clamp_min_(0.0)

    def mle(self, stim, voxel, lr=0.025, n_iter=250, n_print=50):
        '''
        Wrapper for maximum likelihood estimation
        '''
        warn(('Pure gradient descent optimization is deprecated. '
             'Use @mle_bnd method instead for better convergence.'),
             DeprecationWarning, stacklevel=2)

        # initialize noise model parameters
        sigma = torch.ones(voxel.shape[0], dtype=torch.float32, requires_grad=True, device=self.device)
        rho = torch.tensor(0.1, dtype=torch.float32, requires_grad=True, device=self.device)
        chnl = torch.tensor(0.25, dtype=torch.float32, requires_grad=True, device=self.device)

        # run mle using gradient descent (SGD optimizer)
        self._mle([rho, sigma, chnl], stim, voxel, lr, n_iter, n_print)

        # save noise model parameters
        self.rho = rho.item()
        self.sigma = sigma.detach().clone()
        self.chnl = chnl.item()
        self.cov = self._cov_mtx(self.rho, self.sigma, self.chnl)

        return self.rho, self.sigma.clone(), self.chnl

    def mle_bnd(self, stim, voxel, verbose=True):
        '''
        Maximum likelihood estimation with scipy bounded optimization
        '''
        # define objective function
        fun = lambda paras : self.obj_wrapper(stim, voxel, paras)

        # define variables
        x0 = np.array([0.10, 0.30, *(0.10 * np.random.random(voxel.shape[0]) + 0.70)])
        bounds = Bounds(lb = [0.01] + [0.05] * (x0.size - 1),
                        ub = [0.90] + [2.5] * (x0.size - 1),
                        keep_feasible=True)

        # run optimization
        # scipy Sequential Least SQuares Programming
        res = minimize(fun, x0, jac=True, bounds=bounds,
                        options={'maxiter':1e4, 'disp':True})

        if verbose:
            print('Success:', res.success, res.message)
            print('Fval:', res.fun)

        # record model parameters
        self.rho = torch.tensor(res.x[0], dtype=torch.float32, device=self.device)
        self.chnl = torch.tensor(res.x[1], dtype=torch.float32, device=self.device)
        self.sigma = torch.reshape(torch.tensor(res.x[2:],
                                    dtype=torch.float32,
                                    device=self.device),
                                    (voxel.shape[0], 1))

        self.cov = self._cov_mtx(self.rho, self.sigma, self.chnl)
        return res

    def obj_wrapper(self, stim, voxel, paras):
        '''
        Objective function with numpy parameter vector
        and gradient returned as numpy vector
        '''
        # create torch variable
        rho = torch.tensor(paras[0], dtype=torch.float32,
                    requires_grad=True, device=self.device)
        chnl = torch.tensor(paras[1], dtype=torch.float32,
                    requires_grad=True, device=self.device)
        sigma = torch.tensor(paras[2:], dtype=torch.float32, device=self.device)
        sigma = torch.reshape(sigma, (voxel.shape[0], 1))
        sigma = sigma.clone().detach().requires_grad_(True)

        # compute loss function
        cov = self._cov_mtx(rho, sigma, chnl)
        loss = self.objective(stim, voxel, cov)
        loss.backward()

        # record gradient
        grad = np.zeros_like(paras)
        grad[0] = rho.grad.cpu()
        grad[1] = chnl.grad.cpu()
        grad[2:] = sigma.grad.flatten().cpu()

        # return loss and gradient value
        return loss.item(), grad