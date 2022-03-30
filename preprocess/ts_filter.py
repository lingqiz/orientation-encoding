import os

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
n_session = 6
file_base = '_Atlas_hp2000_clean.dtseries.nii'
for idx in range(n_session):
    ses_name = 'func-0%d' % (idx + 1)
    ses_dir = os.path.join(base_dir, ses_name)

    if not os.path.exists(ses_dir):
        os.system("mkdir %s" % ses_dir)

    file_name = ses_name + file_base
    file_path = os.path.join(ses_dir, file_name)
    if not os.path.exists(file_path):
        source_path = os.path.join(base, file_name)
        os.system("mv %s %s" % (source_path, ses_dir))

# Create a zip file
os.chdir(os.path.join(base, 'Filtered'))
if not os.path.exists('%s.zip' % sub_name):
    os.system("zip -r %s %s" % (sub_name, sub_name))