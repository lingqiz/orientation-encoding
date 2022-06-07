import os, json, einops, numpy as np
import scipy.io as sio

# Define useful constants
N_ACQ = 30; N_TRIAL = 39
N_DROP = {'mtSinai':-4, 'glm':-1}

# Note the duplication of these also in tilt_orient.py
STIM_PATH = os.path.join('.', 'experiment', 'stim_seq.txt')
STIM_VAL = np.array([55, 105, 15, 155, 85, 135, 145, 95, 165,
        45, 25, 35, 65, 115, 5, 125, 75, 175]).astype(np.double)

# load experimental design information
with open(STIM_PATH, 'r') as seq_file:
    STIM_SEQ = seq_file.read().replace('\n', ' ').split()
    STIM_SEQ = np.array(list(map(int, STIM_SEQ))).reshape([-1, N_TRIAL - 1])

# return data path
def _data_path(sub_name):
    path = [os.path.expanduser('~'), 'Data', 'fMRI', sub_name]
    return os.path.join(*path)

# load the GLM results in standard format
def load_glm(sub_name, model_type='mtSinai'):
    data_path = _data_path(sub_name)

    response = []
    session = 'NeuralCoding%02d'
    for idx in range(3):
        # read GLM fits
        fl_name = '%s_%s_%s.mat' % (model_type, sub_name, session % (idx + 1))
        model_fit = sio.loadmat(os.path.join(data_path, fl_name))['results'][0][0]

        if idx == 0:
            v_label = model_fit['v_label']
            e_label = model_fit['e_label']
        glm_beta = model_fit['params']

        # GLM weights on stimulus
        response.append(glm_beta[:, :N_DROP[model_type]])

    # group response by acquisition
    # n trial per acquisition = 39
    response = np.hstack(response)
    response = response.reshape([response.shape[0], N_ACQ, N_TRIAL])

    return response, v_label.flatten(), e_label.flatten()

# load the sequence of responses for each condition
def load_response(sub_name, model_type='mtSinai'):
    # load data
    response, v_label, e_label = load_glm(sub_name, model_type)
    stim_seq, stim_val, cond_seq = load_exp(sub_name)

    # produce stimulus sequence
    stim_val = np.append(stim_val, -1)
    stim_seq = stim_val[stim_seq.flatten() - 1]
    stim = stim_seq[stim_seq != -1]

    all_resp = []
    for idx in range(3):
        # get the response for each condition, drop the first response
        cond_resp = response[:, cond_seq == idx, 1:]
        cond_resp = einops.rearrange(cond_resp, 'vox acq stim -> vox (acq stim)')

        # rearrange into shape (n_voxel by n_trial), drop the baseline response
        all_resp.append(cond_resp[:, stim_seq != -1])

    return stim, all_resp, v_label, e_label

# load experiment setup information
def load_exp(sub_name):
    # load json file
    json_path = os.path.join(_data_path(sub_name), '%s.json' % sub_name)
    with open(json_path, 'r') as json_file:
        cond_seq = np.array(json.load(json_file)['Cond_Seq'])

    return STIM_SEQ, STIM_VAL, cond_seq

# sort the data by stim condition and values
def sort_response(stim_key, stim_seq, cond_seq, response):
    all_resp = []
    for cond_idx in range(3):
        # response for cond_idx, drop the first response
        cond_resp = response[:, cond_seq == cond_idx, 1:]
        cond_resp = cond_resp.reshape([cond_resp.shape[0], -1])

        # sort data by stimulus condition
        n_repeat = cond_resp.shape[1] / len(stim_key)

        resp = np.zeros([len(stim_key), cond_resp.shape[0], int(n_repeat)])
        for idx in range(len(stim_key)):
            resp[idx] = cond_resp[:, stim_seq == stim_key[idx]]

        # add to all response
        all_resp.append(resp)

    return all_resp