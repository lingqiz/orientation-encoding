from psychopy import core, visual, gui, data, event
from psychopy.hardware import keyboard

import numpy as np 
import random

from sampler import sample_orientation

# create window and stimuli
# show welcome message and instruction
n_trial = 500

win = visual.Window([1920, 1080], allowGUI=True, monitor='testMonitor', units='deg')

welcome = visual.TextStim(win, pos=[0,-5], \
    text='Thanks for your time. Press any key to continue.')   
inst1 = visual.TextStim(win, pos=[0,+5], \
    text='You will first see a quickly flashed gabor stimulus.')
inst2 = visual.TextStim(win, pos=[0,0], \
    text='After the stimulus, adjust the prob using <-- and --> to match its orientation.')

welcome.draw()
inst1.draw()
inst2.draw()

win.flip()
event.waitKeys()

# run experiment with stimulus
target = visual.GratingStim(win, sf=1, size=10, mask='gauss', contrast=0.1)
fixation = visual.GratingStim(win, color=-1, colorSpace='rgb', tex=None, mask='circle', size=0.2)
message = visual.TextStim(win, pos=[0, +10], text='use <-- and --> key for response')

kb = keyboard.Keyboard()
for idx in range(n_trial):
    # ISI for 500 ms
    fixation.draw()
    win.flip()
    core.wait(1.0)
    
    # Draw stimulus for 200 ms
    targetOri = float(sample_orientation(n_sample=1, uniform=True))
    target.setOri(targetOri)
    target.draw()
    fixation.draw()
    win.flip()
    core.wait(0.2)

    # blank screen for 1s
    fixation.draw()
    win.flip()
    core.wait(1.0)
            
    # get response
    resp_ori = int(sample_orientation(n_sample=1, uniform=True))
    prob = visual.Line(win, start=(-1.50, -1.50), end=(1.50, 1.50), lineWidth=10.0, \
        lineColor='black', size=1, ori=resp_ori, contrast=0.75)
    
    message.draw()
    prob.draw()
    win.flip()
    
    def resp_callback(increment, current_val, prob):        
        return_val = (current_val + increment) % 180
        prob.setOri(return_val)

        return return_val
        
    resp_flag = True
    kb.clearEvents()
    while resp_flag:
        allKeys = kb.getKeys(['right', 'left', 'space', 'escape'], waitRelease=True)
        for thisKey in allKeys:
            if thisKey=='space':
                # confirm response
                resp_flag = False

            elif thisKey == 'left':
                resp_ori = resp_callback(-1, resp_ori, prob)

            elif thisKey == 'right':
                resp_ori = resp_callback(+1, resp_ori, prob)

            elif thisKey == 'escape':
                # abort experiment
                core.quit()  
        
            message.draw()
            prob.draw()
            win.flip()
