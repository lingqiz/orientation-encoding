import sys
from local_utils import *

# Initialize flywheel client
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Get the gear and set analysis label
gear = fw.lookup('gears/bayesprf/0.2.5')
analysis_label = 'Bayes_pRF %s' % gear.gear.version

# Only run on specified subjects
# given by command line argument
sub_list = sys.argv
sub_list.pop(0)

# Iterate and record all sessions, sort by subject
all_data = get_all_data(project)

for sub_label in all_data.keys():
    # Only run on specified subjects
    if sub_label not in sub_list:
        continue

    # Run Bayes pRF on subject's population RF fits
    prf_ses = all_data[sub_label]['pRF']
    analyses = prf_ses.analyses

    # Get pRF model fits and structural data
    file_index = 3
    pRF_model = None
    struct_data = None

    for ana in analyses:
        # Get the result for hcp_struct
        if ana.label.starts_with('hcp-struct'):
            struct_data = ana.get_file(sub_label + '_hcpstruct.zip')

        # Get the result from forward model
        if ana.label.starts_with('ForwardModel'):
            print(ana.label)
            pRF_model = ana.files[file_index]

    # Run the Bayes pRF gear
    inputs = {'structZip':struct_data, 'nativeMgzMaps':pRF_model}
    config = {'min-input-eccen':0, 'max-input-eccen':8.0, 'weight-min':0.1,
              'scale':100, 'field-sign-weight':1.0, 'radius-weight':0.25}

    if get_response('Bayes pRF'):
        print('\nSubmitting forward model for %s' % sub_label)
        gear.run(analysis_label=analysis_label, config=config,
                 inputs=inputs, destination=prf_ses)