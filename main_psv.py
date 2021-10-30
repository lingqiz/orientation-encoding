from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')

sub_val = str(sys.argv[1])

# two blocks, about half an hour each
n_trial = 150
n_block = 2
exp = PriorLearningKeyboard(sub_val=sub_val, n_trial=n_trial)

# start running the experiment
# passive viewing condition
exp.mode = 'uniform'
exp.record_resp = False
exp.atten_task = True

# change the message for passive viewing
exp.welcome.text = 'Press "space" to contiune.'
exp.inst1.text = 'You will see a sequence of flashed gabor stimulus.'
exp.inst2.text = 'Try to maintain fixation at the center dot.'

exp.stim_dur = 1.5
exp.delay = 4.5

exp.start()
for block in range(n_block):
    exp.run()
    exp.save_data()

    if block < n_block - 1:
        exp.pause()

exp.end()