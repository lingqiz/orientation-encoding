import sys
from local_utils import *

# Initialize flywheel client
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Get the gear and analysis label
gear = fw.lookup('gears/hcp-icafix/0.2.1_rc2')
analysis_label = 'hcp-icafix %s' % gear.gear.version

# Only run on specified subjects
# given by command line argument
sub_list = sys.argv
sub_list.pop(0)

# Iterate and record all sessions, sort by subject
all_data = get_all_data(project)

# Run ICAFIX gear on subject, separate by session
for sub_label in all_data.keys():
    # Only run on specified subjects
    if sub_label not in sub_list:
        continue
    print('\nRunning icafix gear for subject: %s' % sub_label)

    # Run gear for pRF session
    # Get analysis for the pRF session
    if not 'pRF' in all_data[sub_label].keys():
        print('No pRF session found for subject: %s' % sub_label)
        continue

    prf_ses = all_data[sub_label]['pRF']
    analyses = prf_ses.analyses

    func_data = []
    struct_data = None
    for ana in analyses:
        # get the result for hcp_struct
        if ana.label.startswith('hcp-struct'):
            struct_data = ana.get_file(sub_label + '_hcpstruct.zip')

        # get all function runs
        if ana.label.startswith('hcp-func'):
            func_data.append(ana)

    # Run the gear on pRF session if confrimed by the user
    if get_response('pRF'):
        # split the run into two parts
            split_idx = len(func_data) // 2
            data_pair = (func_data[:split_idx], func_data[split_idx:])

            # run the gear
            for idx, data in enumerate(data_pair):
                submit_icafix(gear, sub_label, 'pRF', analysis_label,
                        prf_ses, data, struct_data, time_stamp, idx)

    # Run gear for NeuralCoding session if confrimed by the user
    if get_response('NeuralCoding'):
        # deprecated: we are not using ICAFIX for orientation stimulus session
        n_session = 3
        for idx in range(n_session):
            ses_label = 'NeuralCoding0%s' % (idx + 1)
            if ses_label not in all_data[sub_label].keys():
                print('No %s session found for subject: %s' % (ses_label, sub_label))
                continue

            stim_ses = all_data[sub_label][ses_label]
            func_data = []

            print('\nFinding acquisitions for %s' % ses_label)
            analyses = stim_ses.analyses
            for ana in analyses:
                # get all function runs and list them
                if ana.label.startswith('hcp-func'):
                    func_data.append(ana)
                    print(ana.label)

            # Run the gear if confrimed by the user
            if get_response(ses_label):
                # split the run into two parts
                split_idx = len(func_data) // 2
                data_pair = (func_data[:split_idx], func_data[split_idx:])

                # run the gear
                for idx, data in enumerate(data_pair):
                    submit_icafix(gear, sub_label, ses_label, analysis_label,
                                stim_ses, data, struct_data, time_stamp, idx)