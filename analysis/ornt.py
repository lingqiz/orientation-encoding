import os, json, numpy as np
import scipy.io as sio
import torch.autograd as autograd
from analysis.encode import *
from analysis.svr import *
from tqdm.notebook import tqdm

# Parameters of the experiment
N_SESSION = 6
N_RUNS = 10
N_TRIAL = 20
N_COND = 3
SES_NAME = 'Neural%02d'

def load_data(sub_name, model_type, roi_name=None):
    '''
    load the behavioral and neural data from file
    for a single subject specified by sub_name
    '''
    # base data path
    data_path = os.path.join(*[os.path.expanduser('~'), 'Data', 'fMRI', 'ORNT', sub_name])

    # load behavioral data
    fl_name = os.path.join(data_path, sub_name + '.json')
    # Load JSON file
    with open(fl_name, 'r') as fl:
        data = json.load(fl)

    # stimulus sequence array
    stim = np.array(data['Stim_Seq'])
    stim = np.reshape(stim, (N_COND, -1)).astype(np.double)
    cond = np.array(data['Cond_List'])
    assert(cond.size == N_SESSION * N_RUNS)

    # load neural data
    if roi_name is not None:
        data_path = os.path.join(data_path, 'roi', roi_name)

    all_response = []
    for idx in range(N_SESSION):
        # file name
        fl_name = '%s_%s.mat' % (model_type, SES_NAME % (idx + 1))

        # beta weights
        model_fit = sio.loadmat(os.path.join(data_path, fl_name))['results'][0][0]
        all_response.append(model_fit['params'].T)

    # all beta response weight
    beta = np.concatenate(all_response, axis=0)
    n_voxel = beta.shape[1]

    # reshape into (N_RUN, N_TRIAL, N_VOXEL)
    beta = np.reshape(beta, (N_SESSION * N_RUNS, N_TRIAL, n_voxel))

    # sort by condition
    beta_sorted = []
    for idx in range(N_COND):
        beta_cond = beta[cond == idx].reshape((-1, n_voxel))
        beta_sorted.append(beta_cond)

    beta_sorted = np.stack(beta_sorted)
    return (stim.astype(float),
            beta_sorted.astype(float))

def cv_decode(stimulus, response, batchSize, device):
    '''
    Cross-validated orientation decoding based on the forward encoding model
    '''
    nFold = int(stimulus.shape[0] / batchSize)

    decode_stim = []
    decode_esti = []
    decode_stdv = []

    for idx in tqdm(range(nFold)):
        # leave-one-run-out cross-validation
        hold = np.arange(idx * batchSize, (idx + 1) * batchSize, step=1)
        binary = np.ones(stimulus.shape[0]).astype(bool)
        binary[hold] = False

        stim_tr, resp_tr = (stimulus[binary], response[:, binary])
        stim_ts, resp_ts = stimulus[~binary], response[:, ~binary]

        # fit the encoding model
        model = VoxelEncode(n_func=8, device=device)
        model.ols(stim_tr, resp_tr, lda=0.0)
        model.mle_bnd(stim_tr, resp_tr, verbose=False)

        # run deocding for validation trial
        for idy in range(resp_ts.shape[1]):
            est, std, _ = model.decode(resp_ts[:, idy], method='mean')

            decode_stim.append(stim_ts[idy])
            decode_esti.append(est)
            decode_stdv.append(std)

    return np.array(decode_stim), np.array(decode_esti), np.array(decode_stdv)

def svr_decode(stimulus, response, batchSize):
    '''
    Cross-validated decoding based on support vector regression
    '''
    nFold = int(stimulus.shape[0] / batchSize)

    decode_stim = []
    decode_esti = []

    for idx in tqdm(range(nFold)):
        # leave-one-run-out cross-validation
        hold = np.arange(idx * batchSize, (idx + 1) * batchSize, step=1)
        binary = np.ones(stimulus.shape[0]).astype(bool)
        binary[hold] = False

        stim_tr, resp_tr = (stimulus[binary], response[:, binary])
        stim_ts, resp_ts = stimulus[~binary], response[:, ~binary]

        # fit the decoding model with SVR
        model = RegressDecode()
        model.fit_model(stim_tr, resp_tr)

        # run deocding for validation trial
        est = model.decode(resp_ts)
        decode_stim.append(stim_ts)
        decode_esti.append(est)

    return np.concatenate(decode_stim), np.concatenate(decode_esti)

def llhd_derivative(stimulus, response, batchSize, device, pbar=True):
    '''
    Compute the first and second derivative for the likelihood of each trial,
    based on the model fit on the training set
    '''
    nFold = int(stimulus.shape[0] / batchSize)

    # record the derivative value
    stim_val = []
    fst_dev = []
    snd_dev = []

    for idx in tqdm(range(nFold), disable=(not pbar)):
        # leave-one-run-out cross-validation
        hold = np.arange(idx * batchSize, (idx + 1) * batchSize, step=1)
        binary = np.ones(stimulus.shape[0]).astype(bool)
        binary[hold] = False

        stim_tr, resp_tr = (stimulus[binary], response[:, binary])
        stim_ts, resp_ts = stimulus[~binary], response[:, ~binary]

        # fit four models with shifted tuning curve
        # to correct for potential bias in the model
        shift_vals = np.linspace(0, 1, 4, endpoint=False)
        for shift in shift_vals:
            model = VoxelEncode(n_func=8, shift=shift, device=device)
            model.ols(stim_tr, resp_tr)
            _ = model.mle_bnd(stim_tr, resp_tr, verbose=False)

            # run deocding for validation trial
            for idy in range(resp_ts.shape[1]):
                stim = torch.tensor([stim_ts[idy]], dtype=torch.float32,
                                    device=device, requires_grad=True)
                resp = torch.tensor(resp_ts[:, idy], dtype=torch.float32,
                                    device=device).unsqueeze(-1)

                # compute likelihood and its derivatives
                log_llhd = model.likelihood(stim, resp)
                fd = autograd.grad(log_llhd, stim, create_graph=True)[0]
                sd = autograd.grad(fd, stim)[0]

                # save results
                stim_val.append(stim_ts[idy])
                fst_dev.append(fd.item())
                snd_dev.append(sd.item())

    return np.array(stim_val), np.array(fst_dev), np.array(snd_dev)

def slide_average(stim, data, avg_func, window, config):
    '''
    Compute sliding average
    '''
    value = []
    center = config['center']
    for ctr in center:
        # define window
        bin_lb = ctr - window
        bin_ub = ctr + window

        # indexing into the data
        if config['cyclical']:
            if bin_lb < config['lb']:            
                index = np.logical_or(stim >= bin_lb + config['cycle'], stim < bin_ub)
            elif bin_ub > config['ub']:
                index = np.logical_or(stim >= bin_lb, stim < bin_ub - config['cycle'])
            else:
                index = np.logical_and(stim >= bin_lb, stim < bin_ub)
        else:
            index = np.logical_and(stim >= bin_lb, stim < bin_ub)

        # compute statistics
        value.append(avg_func(data[index]))

    # return bin center and value
    center = np.copy(config['center'])
    center[0] = config['lb']
    center[-1] = config['ub']
    return center, np.array(value)