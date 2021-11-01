from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')

sub_val = str(sys.argv[1])

n_trial = 120
exp = OrientEncodeKeyboard(sub_val=sub_val, n_trial=n_trial)

# start running the experiment
# passive viewing condition
exp.mode = 'uniform'
exp.record_resp = False
exp.atten_task = True

# change the message for passive viewing
exp.welcome.text = 'Press "space" to contiune.'
exp.inst1.text = 'You will see a sequence of flashed gabor stimulus.'
exp.inst2.text = 'Try to maintain fixation at the center dot.'

# exp condition
# 5s trial duration
exp.stim_dur = 1.5
exp.delay = 3.5

# run experiment
exp.start()
exp.run()
exp.end()