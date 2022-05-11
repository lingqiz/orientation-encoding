import os, json, numpy as np
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
        model_fit = sio.loadmat(os.path.join(data_path, fl_name))
        model_fit = model_fit['results'][0][0]['params']

        # GLM weights on stimulus
        response.append(model_fit[:, :N_DROP[model_type]])

    # group response by acquisition
    # n trial per acquisition = 39
    response = np.hstack(response)
    response = response.reshape([response.shape[0], N_ACQ, N_TRIAL])

    return response

# load experiment setup information
def load_exp(sub_name):
    # load json file
    json_path = os.path.join(_data_path(sub_name), 'LQZ.json')
    with open(json_path, 'r') as json_file:
        cond_seq = np.array(json.load(json_file)['Cond_Seq'])

    return STIM_SEQ, STIM_VAL, cond_seq
