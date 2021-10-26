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

exp.start()
for block in range(n_block):
    exp.run()
    exp.save_data()

    if block < n_block - 1:
        exp.pause()

exp.end()