import flywheel, datetime, sys
from local_utils import *

# flywheel API key
flywheel_API = load_key()

# Initialize
time_stamp = datetime.datetime.now().strftime("%y/%m/%d_%H:%M")
fw = flywheel.Client(flywheel_API)
project = fw.projects.find_first('label=orientation_encoding')

# Get the gear and analysis label
gear = fw.lookup('gears/hcp-icafix/0.2.0')
analysis_label = 'hcp-icafix %s' % gear.gear.version

# Only run on specified subjects
# given by command line argument
sub_list = sys.argv
sub_list.pop(0)

# Iterate and record all sessions, sort by subject
all_data = {}
for session in project.sessions.iter():

    # Because we want information off the sessions's analyses, we need to reload
    # The container to make sure we have all the metadata.
    session = session.reload()
    sub_label = session.subject.label
    ses_label = session.label

    # store the sessions
    if sub_label not in all_data.keys():
        all_data[sub_label] = {}

    all_data[sub_label][ses_label] = session

# Run ICAFIX gear on subject, separate by session
for sub_label in all_data.keys():
    # Only run on specified subjects
    if sub_label not in sub_list:
        continue

    print('\nRunning icafix gear for subject: %s' % sub_label)

    # Run gear for pRF session
    # Get analysis for the pRF session
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

    # Run the gear if confrimed by the user
    if get_response('pRF'):
        # split the run into two parts
        split_idx = len(func_data) // 2
        data_pair = (func_data[:split_idx], func_data[split_idx:])

        # run the gear
        for data in data_pair:
            submit_icafix(gear, sub_label, 'pRF', analysis_label,
                        prf_ses, data, struct_data, time_stamp)

    # Run gear for NeuralCoding session
    label = 'NeuralCoding'
    n_session = 3
    for idx in range(n_session):
        ses_label = 'NeuralCoding0%s' % (idx + 1)
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
            submit_icafix(gear, sub_label, ses_label, analysis_label,
                        stim_ses, func_data, struct_data, time_stamp)