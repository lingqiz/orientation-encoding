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