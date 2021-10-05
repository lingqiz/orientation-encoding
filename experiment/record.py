from tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')

sub_val = str(sys.argv[1])
n_trial = 10
exp = PriorLearningKeyboard(sub_val=sub_val, n_trial=n_trial)

# start running the experiment
exp.mode = 'uniform'
exp.record = True

exp.start()
exp.run()
exp.end()