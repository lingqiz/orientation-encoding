from prior_learning import *

# create the experiment with n_trial and uniform/non-uniform
# learning conditions
experiment = PriorLearningKeyboard(n_trial=5, uniform=True)

# running the experiment
experiment.start()

# learning block with natural orientation prior
experiment.uniform = False
experiment.run()

experiment.pause()

# learning block with uniform prior
experiment.uniform = True
experiment.run()

# end and record the experiment
experiment.end()