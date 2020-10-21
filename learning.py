from psychopy import core, visual, gui, data, event

import numpy as np 
import random

from sampler import sample_orientation

# create window and stimuli
win = visual.Window([1920, 1080], allowGUI=True, monitor='testMonitor', units='deg')
target = visual.GratingStim(win, sf=1, size=4, mask='gauss', ori=expInfo['refOrientation'])