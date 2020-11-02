from prior_learning import *

# create the experiment with n_trial for each block
experiment = PriorLearningKeyboard(n_trial=5)

# start running the experiment
experiment.start()

# unifrom without feedback
experiment.mode = 'uniform'
experiment.show_fb = False
experiment.run()

experiment.pause()

# learning block with novel stim distribution
experiment.mode = 'oblique'
experiment.show_fb = True
experiment.run()

experiment.pause()

# uniform without feedback
experiment.mode = 'uniform'
experiment.show_fb = False
experiment.run()

# end and record the experiment
experiment.end()