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
# Second argument is mag_factor
para_list = sys.argv
para_list.pop(0)

sub_list = [para_list[0]]
mag_factor = float(para_list[1])

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
    func_data = []
    ts_filter = None
    struct_data = None

    # Get the ICAFIX data and struct data
    for ana in analyses:
        # Get the result for hcp_struct
        if ana.label.startswith('hcp-struct'):
            struct_data = ana.get_file(sub_label + '_hcpstruct.zip')

        # Get all function runs
        if ana.label.startswith('hcp-icafix'):
            print(ana.label)
            func_data.append(ana.files[func_index])

        # Get the result for TS Filter
        if ana.label.startswith('TS Filter'):
            print(ana.label)
            ts_filter = ana.files[0]

    # Submit the forward model gear
    # Set up input parameters for submit forward model gear
    icafix = True
    # Use ICAFIX output as input
    if icafix:
        gain = '300'
        inputs = {'funcZip01':func_data[0], 'funcZip02':func_data[1],
                'maskFile':va_mask, 'stimFile':prf_stim, 'structZip':struct_data}
    # Use simple filtered output as input
    else:
        gain = '1'
        inputs = {'funcZip01':ts_filter, 'maskFile':va_mask,
                'stimFile':prf_stim, 'structZip':struct_data}

    # Gear config
    # Need to change the screen magnification factor and/or HRF parameters
    modelOpts = '(pixelsPerDegree),5.1751,(polyDeg),5,(typicalGain),%s,' \
                '(screenMagnification),%.5f' % (gain, mag_factor)

    config = {'averageAcquisitions':'1', 'convertToPercentChange':'0', 'tr':'0.8',
              'modelClass':'prfTimeShift', 'modelOpts':modelOpts, 'trimDummyStimTRs':'0'}

    # Submit the gear
    if get_response('forward model pRF'):
        print('\nSubmitting forward model for %s' % sub_label)
        gear.run(analysis_label=analysis_label, config=config,
            inputs=inputs, destination=prf_ses, tags=['large'])