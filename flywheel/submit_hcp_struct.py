import flywheel
import datetime

# flywheel API key
with open('flywheel.key') as fl:
    flywheel_API = fl.readlines()[0]

# Initialize gear stuff, get the project and subjects
fw = flywheel.Client(flywheel_API)
proj = fw.projects.find_first('label=orientation_encoding')
subjects = proj.subjects()

# Get the analysis gear
qp = fw.lookup('gears/hcp-struct/0.1.8')

# Get the date and time to post in the analysis label and construct the label
# from date and gear name/version
now = datetime.datetime.now().strftime("%y/%m/%d_%H:%M")
analysis_label = 'hcp-struct %s %s' % (qp.gear.version, now)

# Get the freesurfer license and set config
freesurfer_license = proj.get_file('freesurfer_license.txt')
config = {'RegName': 'FS',
          'Subject': 'NA'}

# Get the sessions that already has hcp-struct gears
analyses = fw.get_analyses('projects', proj.id, 'sessions')
struct = [ana for ana in analyses if ana.label.startswith('hcp-struct')]
sessions_that_have_struct = []
for s in struct:
    sessions_that_have_struct.append(s.parent.id)


# Loop through subjects and get sessions
for subject in subjects:
    sessions = subject.sessions()
    # Loop through sessions and get acquisitions
    for session in sessions:
        acquisition_list=[]
        acquisitions = session.acquisitions()
        # Put all acquisitions in the acquisition list
        for acquisition in acquisitions:
            acquisition_list.append(acquisition.label)
        # Check if T1 and T2 images exist in the current session. Also check
        # if the hcpstruct run already exists in the run
        if 'anat-T1w_acq-axial' in acquisition_list and 'anat-T2w_acq-spc' in acquisition_list and not session.id in sessions_that_have_struct:
            destination = session
            # Loop through the acquisitions
            for acquisition in acquisitions:
                # Get the T1 container and find the nifti image in it
                if 'anat-T1w_acq-axial' in acquisition.label:
                    files = acquisition.files
                    for file in files:
                        if 'nii.gz' in file.name:
                            T1_image = file
                # Get the T2 container and the nifti image in it
                if 'anat-T2w_acq-spc' in acquisition.label:
                    files = acquisition.files
                    for file in files:
                        if 'nii.gz' in file.name:
                            T2_image = file

            # Get the subject name and use it into the subject config
            config['Subject'] = subject.label

            # Compule all the inputs together
            inputs = {'FreeSurferLicense': freesurfer_license, 'T1': T1_image, 'T2': T2_image}
            print('submitting HCP-struct for %s' % subject.label)
            # Submit the gear
            try:
                _id = qp.run(analysis_label=analysis_label,
                              config=config, inputs=inputs, destination=destination)
            except Exception as e:
                print(e)
