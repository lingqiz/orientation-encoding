from prior_learning import *

# create the experiment with n_trial for each block
# different class for choices of IO methods 

n_trial = 240
input_type = 'buttons'
if input_type == 'keyboard':
    exp = PriorLearningKeyboard(n_trial=n_trial)
elif input_type == 'buttons':
    exp = PriorLearningButtons(n_trial=n_trial)
elif input_type == 'joystick':
    exp = PriorLearningJoystick(n_trial=n_trial)
else:
    raise ValueError('invalid input method')

# start running the experiment
exp.start()

# learning block with novel stim distribution
exp.mode = 'cardinal'
# exp.mode = 'oblique'

exp.show_fb = True
exp.run()

exp.pause()

# learning block with novel stim distribution
exp.mode = 'cardinal'
# exp.mode = 'oblique'

exp.show_fb = True
exp.run()

exp.pause()

# learning block with novel stim distribution
exp.mode = 'cardinal'
# exp.mode = 'oblique'

exp.show_fb = True
exp.run()

# end and record the experiment
exp.end()