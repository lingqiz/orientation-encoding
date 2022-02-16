import flywheel, datetime, sys

# flywheel API key
with open('flywheel.key') as fl:
    flywheel_API = fl.readlines()

# Initialize
time_stamp = datetime.datetime.now().strftime("%y/%m/%d_%H:%M")
fw = flywheel.Client(flywheel_API)
project = fw.projects.find_first('label=orientation_encoding')

# Get the gear and analysis label
qp = fw.lookup('gears/hcp-icafix/0.1.7')
analysis_label = 'hcp-icafix %s' % qp.gear.version

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

    print('Run icafix gear for subject: %s' % sub_label)

    # Run gear for pRF session
    # Get analysis for the pRF session
    prf_ses = all_data[sub_label]['pRF']
    analyses = prf_ses.analyses

    func_data = []
    struct = None
    for ana in analyses:
        # get the result for hcp_struct
        if ana.label.startswith('hcp-struct'):
            struct = ana.get_file(sub_label + '_hcpstruct.zip')

        # get all function runs
        if ana.label.startswith('hcp-func'):
            func_data.append(ana)

    # Set gear config
    config = {'FIXClassifier': 'HCP_hp2000', 'HighPassFilter': 2000,
    'PreserveOnError': True, 'RegName': 'FS', 'Subject': sub_label}

    # Input parameters for submit pRF gear
    inputs = {'StructZip': struct, 'FuncZip': func_data[0].files[6]}
    for idx in range(1, len(func_data)):
        inputs['FuncZip%s' % (idx + 1)] = func_data[idx].files[6]

    # Run icafix for pRF
    new_label = analysis_label + ' [%s_pRF]' % sub_label + ' ' + time_stamp
    qp.run(analysis_label=new_label, config=config, inputs=inputs, destination=prf_ses)
    print('Submitting pRF for %s' % sub_label)

    # Run icafix for stim run
    label = 'NeuralCoding'
    n_session = 3
    func_data = []
    for idx in range(n_session):
        ses_label = 'NeuralCoding0%s' % (idx + 1)
        stim_ses = all_data[sub_label][ses_label]

        analyses = stim_ses.analyses
        for ana in analyses:
            # get all function runs
            if ana.label.startswith('hcp-func'):
                func_data.append(ana)

    for func_acq in func_data:
        # running icafix on actual stimView data
        print(func_acq.label)
