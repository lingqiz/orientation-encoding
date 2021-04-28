from prior_learning import *
import sys

# create the experiment with n_trial for each block
# different class for choices of IO methods 
if not len(sys.argv) == 2:
    raise ValueError('Incorrect number of input arguments')
    
sub_val = str(sys.argv[1])
n_trial = 200
input_type = 'buttons'
if input_type == 'keyboard':
    exp = PriorLearningKeyboard(sub_val=sub_val, n_trial=n_trial)
elif input_type == 'buttons':
    exp = PriorLearningButtons(sub_val=sub_val, n_trial=n_trial)
elif input_type == 'joystick':
    exp = PriorLearningJoystick(sub_val=sub_val, n_trial=n_trial)
else:
    raise ValueError('invalid input method')

# 'uniform', 'cardinal' or 'oblique'
# with feedback (True) or without (False)
exp.mode = 'oblique'
exp.show_fb = True

# start running the experiment
exp.start()

# learning block with novel stim distribution and feedback
# block 1
exp.run()
exp.save_data()
exp.pause()

# learning block with novel stim distribution and feedback
# block 2
exp.run()
exp.save_data()
exp.pause()

# learning block with novel stim distribution and feedback
# block 3
exp.run()

# end and record the experiment
exp.end()