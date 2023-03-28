import os, json, numpy as np
import scipy.io as sio

# Parameters of the experiment
N_SESSION = 6
N_RUNS = 10
N_TRIAL = 20
N_COND = 3
SES_NAME = 'Neural%02d'

def load_data(sub_name, model_type):
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
    return (stim, beta_sorted)