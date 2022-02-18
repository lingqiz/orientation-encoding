import flywheel
import datetime
from local_utils import *

# flywheel API key
flywheel_API = load_key()

# Initialize gear stuff
now = datetime.datetime.now().strftime("%y/%m/%d_%H:%M")
fw = flywheel.Client(flywheel_API)

# Find subjects
proj = fw.projects.find_first('label=orientation_encoding')
subjects = proj.subjects()

# Find analyses
analyses = fw.get_analyses('projects', proj.id, 'sessions')
struct = [ana for ana in analyses if ana.label.startswith('hcp-struct')]
func = [ana for ana in analyses if ana.label.startswith('hcp-func')]

# Find the sessions that already have func
sessions_that_have_func = []
for f in func:
    sessions_that_have_func.append(f.parent.id)

# Set gear name and analysis label
qp = fw.lookup('gears/hcp-func/0.1.7')
analysis_label = 'hcp-func %s' % qp.gear.version

# Get freesurfer license and gradient coefficients
freesurfer_license = proj.get_file('freesurfer_license.txt')
coef_grad = proj.get_file('coeff.grad')

# Loop through subjects
for subject in subjects:
    # Find the hcp_struct information
    subject_id = subject.label
    for st in struct:
        if subject.id == st.parents.subject:
            struct_gear = st
            struct_result = struct_gear.get_file(subject_id + '_hcpstruct.zip')

    # Loop through sessions and run hcp_func if not already done
    sessions = subject.sessions()
    for session in sessions:
        if session.id not in sessions_that_have_func:
            # Loop through acquisitions and get the spin echo images
            acquisitions = session.acquisitions()

            # Get the two spin echos field map in the session
            for acquisition in acquisitions:
                if acquisition.label == 'fmap_dir-AP_acq-SpinEchoFieldMap':
                    spin_echo_negative = acquisition
                    for i in spin_echo_negative.files:
                        if 'nii.gz' in i.name:
                            spin_echo_negative = i
                if acquisition.label == 'fmap_dir-PA_acq-SpinEchoFieldMap':
                    spin_echo_positive = acquisition
                    for i in spin_echo_positive.files:
                        if 'nii.gz' in i.name:
                            spin_echo_positive = i

            # Loop through the acquisitions again and get the runs
            for acquisition in acquisitions:
                if 'func_task' in acquisition.label and 'SBRef' not in acquisition.label and 'PhysioLog' not in acquisition.label:
                    fmri_acq = acquisition
                    acq_number = fmri_acq.label[-2:]
                    acq_direction = fmri_acq.label[-9:-7]
                    for i in fmri_acq.files:
                        if 'nii.gz' in i.name:
                            fmri_acq = i

                    for ii in acquisitions:
                        if 'SBRef' in ii.label and acq_number in ii.label and acq_direction in ii.label:
                            scout_image = ii
                            for a in scout_image.files:
                                if 'nii.gz' in a.name:
                                    scout_image = a

                    inputs = {'FreeSurferLicense': freesurfer_license, 'GradientCoeff': coef_grad,
                            'SpinEchoNegative': spin_echo_negative, 'SpinEchoPositive': spin_echo_positive,
                            'StructZip': struct_result, 'fMRIScout': scout_image, 'fMRITimeSeries': fmri_acq}

                    config = {'AnatomyRegDOF': 6, 'BiasCorrection': 'SEBased', 'MotionCorrection': 'MCFLIRT',
                            'RegName': 'FS', 'fMRIName': acquisition.label}

                    new_analysis_label = analysis_label + ' ' + acquisition.label + ' ' + now

                    # Submit the gear
                    print('Submitting %s' % acquisition.label)
                    _id = qp.run(analysis_label=new_analysis_label, config=config,
                                inputs=inputs, destination=session)


