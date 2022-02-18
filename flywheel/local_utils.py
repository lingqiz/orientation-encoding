# a collection of helper functions
# for flywheel gear submission

def load_key():
    """
    Load the flywheel API key from a file
    """
    with open('flywheel.key') as fl:
        return fl.readlines()[0]

def get_response(ses_label):
    """
    Get a response from the user
    """
    response = input('Submit Gear %s? [Y/N] ' % ses_label)
    if response.lower() == 'y':
        return True
    else:
        return False

def submit_icafix(gear, sub_label, ses_label, analysis_label,
    session, func_data, struct_data, time_stamp, run_idx='all'):
    """
    Submit the ICAFIX gear to the flywheel
    """
    # Set gear config
    config = {'FIXClassifier': 'HCP_hp2000', 'HighPassFilter': 2000,
    'PreserveOnError': False, 'RegName': 'FS', 'Subject': sub_label}

    # Input parameters for submit pRF gear
    inputs = {'StructZip': struct_data, 'FuncZip': func_data[0].files[6]}
    for idx in range(1, len(func_data)):
        inputs['FuncZip%s' % (idx + 1)] = func_data[idx].files[6]

    # Run icafix gear on the data
    print('\nSubmitting %s for %s, pt_%s' % (ses_label, sub_label, run_idx))
    label = analysis_label + ' [%s_%s] pt-%s ' % (ses_label, sub_label, run_idx) + time_stamp
    gear.run(analysis_label=label, config=config, inputs=inputs, destination=session, tags=['large'])
