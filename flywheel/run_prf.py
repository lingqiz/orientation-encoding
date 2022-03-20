import sys
from local_utils import *

# Initialize flywheel client
label = 'label=orientation_encoding'
fw, project, time_stamp = flywheel_init(label)

# Get the gear and set analysis label
gear = fw.lookup('gears/forwardmodel/0.12.7')
analysis_label = 'ForwardModel_pRF %s' % gear.gear.version

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

    # Index for the icafix zip file
    func_index = 2
    func_data = None
    struct_data = None

    # Get the ICAFIX data and struct data
    for ana in analyses:
        # get the result for hcp_struct
        if ana.label.startswith('hcp-struct'):
            struct_data = ana.get_file(sub_label + '_hcpstruct.zip')

        # get all function runs
        if ana.label.startswith('hcp-icafix'):
            func_data = ana.files[func_index]

    # Submit the forward model gear
    # Input parameters for submit forward model gear
    inputs = {'funcZip01':func_data, 'maskFile':va_mask,
            'stimFile':prf_stim, 'structZip':struct_data}

    # Gear config
    # Need to change the screen magnification factor and/or HRF parameters
    mag_factor = 0.9125
    modelOpts = '(pixelsPerDegree),5.1751,(polyDeg),5,(screenMagnification),%.5f' % mag_factor

    config = {'averageAcquisitions':1, 'modelClass':'prfTimeShift',
    'modelOpts':modelOpts, 'tr':0.8, 'trimDummyStimTRs':0, 'RegName':'FS'}

    # Submit the gear
    if get_response('forward model pRF : %s' % sub_label):
        print('\nSubmitting forward model for %s' % sub_label)
        gear.run(analysis_label=label, inputs=inputs,
        config=config, destination=prf_ses, tags=['large'])