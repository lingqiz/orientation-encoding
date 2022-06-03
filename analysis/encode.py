import torch, math, einops, numpy as np
from torch.distributions import MultivariateNormal
from torch.autograd.functional import jacobian

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

    def __init__(self, n_func=8):
        '''
        n_func: number of basis functions
        '''
        self.pref = torch.arange(0, 180.0, 180.0 / n_func, dtype=torch.float32)
        self.beta = None

    def forward(self, stim):
        '''
        Predict voxel responses given stimulus value
        '''
        if self.beta is None:
            raise Exception("Model weights are not yet estimated")

        stim = torch.tensor(stim, dtype=torch.float32)
        resp = self.tuning(stim, self.pref)
        return (resp @ self.beta).t()

    def ols(self, stim, voxel):
        '''
        Estimate model weights given stimulus and response
        Stage 1: estimate beta weights using least-square

        stim: stimulus value (n_trial)
        voxel: voxel responses of shape (n_voxel, n_trial)
        '''
        stim = torch.tensor(stim, dtype=torch.float32)
        voxel = torch.tensor(voxel, dtype=torch.float32)

        rgs = self.tuning(stim, self.pref)
        self.beta = torch.linalg.solve(rgs.t() @ rgs, rgs.t() @ voxel.t())

        return self.beta

class VoxelEncodeNoise(VoxelEncodeBase):

    def __init__(self, n_func=8):
        '''
        n_func: number of basis functions
        rho: global noise correlation between voxels
        sigma: vector of noise standard deviations
        '''
        super().__init__(n_func)
        self.rho = 0.0
        self.sigma = None
        self.cov = None

    # multivariate normal distribution negative log-likelihood
    def _log_llhd(self, x, mu, cov):
        return torch.logdet(cov) + (x - mu).t() @ torch.inverse(cov) @ (x - mu)

    # objective function
    def objective(self, stim, voxel, cov):
        voxel = torch.tensor(voxel, dtype=torch.float32)
        mean_resp = super().forward(stim)

        vals = torch.zeros(voxel.shape[1])
        for idx in range(voxel.shape[1]):
            vals[idx] = self._log_llhd(voxel[:, idx], mean_resp[:, idx], cov)

        return torch.sum(vals) / voxel.shape[1]

    # define the covariance matrix (noise model)
    def _cov_mtx(self, rho, sigma):
        return (1 - rho) * torch.diag((sigma ** 2).flatten()) + rho * (sigma @ sigma.t())

    def forward(self, stim):
        # mean response through tuning function
        mean_resp = super().forward(stim)
        sample = torch.zeros_like(mean_resp)

        # sample from multivariate normal distribution
        for idx in range(mean_resp.shape[1]):
            dist = MultivariateNormal(mean_resp[:, idx], self.cov)
            sample[:, idx] = dist.sample()

        return sample

    # estimate noise model
    def mle(self, stim, voxel, n_iter=250, n_print=50):
        '''
        Wrapper for maximum likelihood estimation
        '''
        # initialize noise model parameters
        rho = torch.zeros(1, dtype=torch.float32, requires_grad=True)
        sigma = torch.ones(voxel.shape[0], dtype=torch.float32, requires_grad=True)

        # run mle using gradient descent (Adam optimizer)
        self._mle([rho, sigma], stim, voxel, n_iter, n_print)

        # save noise model parameters
        self.rho = rho.item()
        self.sigma = sigma.detach().clone()
        self.cov = self._cov_mtx(self.rho, self.sigma)

        return self.rho, self.sigma.clone()

    def _clamp(self, rho, sigma):
        '''
        Range constraint
        '''
        with torch.no_grad():
            rho.clamp_(0.0, 1.0 - 1e-6)
            sigma.clamp_min_(1e-6)

    def _mle(self, para, stim, voxel, n_iter, n_print):
        '''
        Estimate model weights given stimulus and response
        Stage 2: estimate noise covariance matrix using maximum likelihood

        stim: stimulus value (n_trial)
        voxel: voxel responses of shape (n_voxel, n_trial)
        '''
        optim = torch.optim.Adam(para, lr=0.01)

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
                print("Iter: {}, Loss: {}".format(iter, loss.item()))
        return

class VoxelEncode(VoxelEncodeNoise):

    def __init__(self, n_func=8):
        super().__init__(n_func)

# some simple testing routines for model fitting
def ols_test(n_func=8, n_voxel=20, n_trial=50):
    '''
    Test OLS estimation part of VoxelEncode
    '''
    simulate = VoxelEncodeBase()
    simulate.beta = torch.rand(n_func, n_voxel)

    stim_val = np.random.rand(n_trial) * 180.0
    resp = simulate.forward(stim_val)

    estimate = VoxelEncodeBase()
    estimate.ols(stim_val, resp.numpy())

    return simulate, estimate