from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    sub_val = str(input('Enter Unique Subject ID:'))
else:
    sub_val = str(sys.argv[1])

N_TRIAL = 20
exp = OrientEncodeKeyboard(sub_val, N_TRIAL)

# start running the experiment
# passive viewing condition
exp.mode = 'uniform'
exp.atten_task = True

# exp condition
# 7s trial duration
exp.stim_dur = 1.5
exp.delay = 10.5
exp.blank = 12.0

# run experiment
exp.start()
exp.run()

print('session length: %.4f' % (exp.session_time))

# save data
exp.end()