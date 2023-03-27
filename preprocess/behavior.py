# convert the raw response file (in JSON) to MAT format for analysis
import sys, os
import json
import numpy as np
from scipy.io import savemat

# Setup directories and file target names
sub_name = sys.argv[-1]
home = os.path.expanduser('~')
base = os.path.join(home, 'Data', 'fMRI', 'ORNT', sub_name)
target = os.path.join(base, sub_name + '.json')

# Load JSON file
with open(target, 'r') as fl:
    data = json.load(fl)

# Reshape data
N_COND = 3
stim = np.array(data['Stim_Seq'])
stim = np.reshape(stim, (N_COND, -1)).astype(np.double)

cond = np.array(data['Cond_List'])
N_RUN = cond.size

# sort response by conditions
resp = np.array(data['Resp_Seq'])
resp = np.reshape(resp, (N_RUN, -1))
resp_sort = np.zeros_like(stim)

for cond_idx in range(3):
    resp_cond = resp[cond == cond_idx, :]
    resp_sort[cond_idx, :] = resp_cond.flatten()

# Save the data in MAT format
save_target = os.path.join(base, sub_name + '.mat')
savemat(save_target, {'stim':stim, 'resp':resp_sort})