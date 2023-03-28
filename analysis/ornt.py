import os, json, numpy as np
import scipy.io as sio
from analysis.encode import *
from tqdm.notebook import tqdm

# Parameters of the experiment
N_SESSION = 6
N_RUNS = 10
N_TRIAL = 20
N_COND = 3
SES_NAME = 'Neural%02d'

def load_data(sub_name, model_type):
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
    return (stim.astype(np.float),
            beta_sorted.astype(np.float))

def cv_decode(stimulus, response, batchSize, device):
    nFold = int(stimulus.shape[0] / batchSize)

    decode_stim = []
    decode_esti = []
    decode_stdv = []

    for idx in tqdm(range(nFold)):
        # leave-one-run-out cross-validation
        hold = np.arange(idx * batchSize, (idx + 1) * batchSize, step=1)
        binary = np.ones(stimulus.shape[0]).astype(np.bool)
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