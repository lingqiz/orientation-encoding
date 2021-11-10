from experiment.tilt_orient import *

# create the experiment with n_trial for each block
sub_val = str(input('Enter Subject ID:'))
condi_id = int(input('Enter Condition ID (0-2):'))
acqst_id = int(input('Enter Acquisition ID (0-9):'))

N_TRIAL = 38
exp = OrientEncodeKeyboard(sub_val, N_TRIAL, condi_id, acqst_id)

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