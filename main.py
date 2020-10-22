from prior_learning import *

# create the experiment with n_trial and uniform/non-uniform
# learning conditions
experiment = PriorLearningKeyboard(n_trial=10, uniform=True)

# running the experiment
experiment.start()
experiment.run()
experiment.end()