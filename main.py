from experiment.tilt_orient import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')

sub_val = str(sys.argv[1])
n_trial = 150
n_block = 4
input_type = 'buttons'
if input_type == 'keyboard':
    exp = PriorLearningKeyboard(sub_val=sub_val, n_trial=n_trial)
elif input_type == 'buttons':
    exp = PriorLearningButtons(sub_val=sub_val, n_trial=n_trial)
elif input_type == 'joystick':
    exp = PriorLearningJoystick(sub_val=sub_val, n_trial=n_trial)
else:
    raise ValueError('invalid input method')

# start running the experiment
exp.mode = 'uniform'
exp.start()

for block in range(n_block):
    exp.run()
    exp.save_data()

    if block < n_block - 1:
        exp.pause()

exp.end()