import os
from local_utils import *

# Current (flywheel) directory
flywheel_path = os.getcwd()

# Setup variables
sub_name = 'HERO_LZ'
acq_type = 'pRF'
home = os.path.expanduser('~')
base = os.path.join(home, 'Data', 'fMRI',
                    sub_name, acq_type)
base_dir = base

# Create file hierarchy
dir_name = ['Filtered', sub_name, 'MNINonLinear', 'Results']
for dir in dir_name:
    base_dir = os.path.join(base_dir, dir)
    if not os.path.exists(base_dir):
        os.system("mkdir %s" % base_dir)

# Move data files to corresponding folders
# This step comes after the MATLAB script
name_list = ''
n_session = 6
file_base = '_Atlas_hp2000_clean.dtseries.nii'
for idx in range(n_session):
    ses_name = 'func-0%d' % (idx + 1)
    ses_dir = os.path.join(base_dir, ses_name)
    name_list += ses_name + ' '

    if not os.path.exists(ses_dir):
        os.system("mkdir %s" % ses_dir)

    file_name = ses_name + file_base
    file_path = os.path.join(ses_dir, file_name)
    if not os.path.exists(file_path):
        source_path = os.path.join(base, file_name)
        os.system("mv %s %s" % (source_path, ses_dir))

# Create config file
config_str = CONFIG_TMPLATE % (name_list, sub_name)
config_fn = '%s__hcpicafix_config.json' % sub_name

os.chdir(os.path.join(base, 'Filtered', sub_name))
if not os.path.exists(config_fn):
    with open(config_fn, 'w') as f:
        f.write(config_str)

# Create a zip file
zip_path = os.path.join(base, 'Filtered', '%s.zip' % sub_name)
os.chdir(os.path.join(base, 'Filtered'))
if not os.path.exists('%s.zip' % sub_name):
    os.system("zip -r %s %s" % (sub_name, sub_name))

# Create analysis and submit to Flywheel
os.chdir(flywheel_path)
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Iterate and record all sessions, sort by subject
all_data = get_all_data(project)

# Update load result to 'TS Filter' analysis
for sub_label in all_data.keys():
    if sub_label != sub_name:
        continue

    # Add analysis and file to pRF session
    prf_ses = all_data[sub_label]['pRF']
    ts_filter = prf_ses.add_analysis(label='TS Filter')
    ts_filter.upload_output(zip_path)