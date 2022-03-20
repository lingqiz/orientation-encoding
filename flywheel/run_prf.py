import sys
from local_utils import *

# Initialize flywheel client
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Get the gear and set analysis label
gear = fw.lookup('gears/forwardmodel/0.12.7')
analysis_label = 'ForwardModel_pRF %s' % gear.gear.version
print(analysis_label)

# Get input variables
va_mask = project.get_file('all_visual_areas_mask.nii')
prf_stim = project.get_file('pRFStimulus_108x108x420.mat')

# Only run on specified subjects
# given by command line argument
sub_list = sys.argv
sub_list.pop(0)

# Iterate and record all sessions, sort by subject
all_data = get_all_data(project)

# Run forward model on subject's pRF data
for sub_label in all_data.keys():
    # Only run on specified subjects
    if sub_label not in sub_list:
        continue

    print('\nRunning forward model pRF for subject: %s' % sub_label)

    # Run gear for pRF session
    # Get analysis for the pRF session
    prf_ses = all_data[sub_label]['pRF']
    analyses = prf_ses.analyses