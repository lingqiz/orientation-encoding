# Download the time series file from FlyWheel
# Useage: python3 ts_get.py SUB_NAME FILE_PREFIX

import sys, os, re
from local_utils import *

# Setup directories
home = os.path.expanduser('~')
base = os.path.join(home, 'Data', 'fMRI')
local_fl = 'func-%02d_Atlas.dtseries.nii'
remote_fl = '%s/MNINonLinear/Results/func-%02d/func-%02d_Atlas.dtseries.nii'

# Initialize flywheel client
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Only run on specified subjects
# given by command line argument
# Second argument is mag_factor
sub_name = sys.argv[-2]
prefix = sys.argv[-1]
suffix = '_func-%02d_hcpfunc.zip'

# Iterate and record all sessions, sort by subject
all_data = get_all_data(project)

# Run forward model on subject's pRF data
for sub_label in all_data.keys():
    # Only run on specified subjects
    if sub_label != sub_name:
        continue

    # Locate Neural sessions
    print('\nDownload time series data for: %s' % sub_label)
    sessions = all_data[sub_label]

    sub_dir = os.path.join(base, sub_label)
    if not os.path.exists(sub_dir):
        os.system("mkdir %s" % sub_dir)

    for ses_name in sessions.keys():
        if ses_name.startswith('Neural0'):
            print(ses_name)
            base_dir = os.path.join(base, sub_label, ses_name)
            analyses = all_data[sub_label][ses_name].analyses

            if not os.path.exists(base_dir):
                os.system("mkdir %s" % base_dir)

            for ana in analyses:
                regex = r'hcp-func.*acq.*run-([0-9][0-9]).*'
                match = re.search(regex, ana.label)
                if match:
                    print(ana.label)
                    run_id = int(match.group(1))

                    # Local file name
                    file_dest= os.path.join(base_dir, local_fl % run_id)
                    # Remote file path
                    file_name = prefix + (suffix % int(match.group(1)))
                    file_path = remote_fl % (prefix, run_id, run_id)

                    # download file
                    ana.download_file_zip_member(file_name, file_path, file_dest)
