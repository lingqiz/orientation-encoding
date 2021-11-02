from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')

sub_val = str(sys.argv[1])

n_trial = 36
acqst_id = 0
exp = OrientEncodeKeyboard(sub_val, n_trial, acqst_id)

# start running the experiment
# passive viewing condition
exp.mode = 'uniform'
exp.atten_task = True

# exp condition
# 5s trial duration
exp.stim_dur = 1.5
exp.delay = 3.5

# run experiment
exp.start()
exp.run()

print('session length: %.4f' % (exp.session_time))

# save data
exp.pause()
exp.end()