from psychopy import core, visual, gui, data, event
import keyboard

import numpy as np 
import random

from sampler import sample_orientation

class PriorLearning:
    '''base class for our prior learning experiment'''
    def __init__(self, n_trial, uniform):
        # will be used for recording response
        self.resp_flag = True
        self.increment = 0

        # parameter for the experiment
        self.n_trial = n_trial
        self.uniform = uniform
        
        # initialize window, message
        self.win = visual.Window([1024, 768], allowGUI=True, monitor='testMonitor', units='deg')
        self.welcome = visual.TextStim(self.win, pos=[0,-5], text='Thanks for your time. Press "space" to continue.')
        self.inst1 = visual.TextStim(self.win, pos=[0,+5], text='You will first see a quickly flashed gabor stimulus.')
        self.inst2 = visual.TextStim(self.win, pos=[0,0], text='After the stimulus, adjust the prob using <-- and --> to match its orientation.')

        # initialize stimulus
        self.target = visual.GratingStim(self.win, sf=0.5, size=10, mask='gauss', contrast=0.1)
        self.fixation = visual.GratingStim(self.win, color=-1, colorSpace='rgb', tex=None, mask='circle', size=0.2)        

        return

    def start(self):
        # show welcome message and instruction
        self.welcome.draw()
        self.inst1.draw()
        self.inst2.draw()
        self.win.flip()

        self.io_wait()

        self.stimulus = np.zeros(self.n_trial)
        self.response = np.zeros(self.n_trial)

        return

    def run(self):
        for idx in range(self.n_trial):
            # ISI for 1000 ms
            self.fixation.draw()
            self.win.flip()
            core.wait(1.0)
            
            # Draw stimulus for 200 ms
            targetOri = sample_orientation(n_sample=1, uniform=self.uniform)
            targetOri = float(targetOri)
            self.stimulus[idx] = targetOri
            
            self.target.setOri(targetOri)
            self.target.draw()
            self.fixation.draw()
            self.win.flip()
            core.wait(0.2)

            # blank screen for 1s            
            self.win.flip()
            core.wait(1.0)

            response = self.io_response()
            self.response[idx] = response

    def end(self):
        print(self.stimulus)
        print(self.response)

    def io_wait(self):
        raise NotImplementedError("method not implemented in the base class")
    
    def io_response(self):
        raise NotImplementedError("method not implemented in the base class")

# implement io method with keyboard
class PriorLearningKeyboard(PriorLearning):
    
    def io_wait(self):
        '''override io_wait'''
        keyboard.wait('space')
        return

    '''override io_response'''
    def io_response(self):
        resp = int(sample_orientation(n_sample=1, uniform=True))

        prob = visual.Line(self.win, start=(0.0, -2.0), end=(0.0, 2.0), lineWidth=5.0, lineColor='black', size=1, ori=resp, contrast=0.75)
        message = visual.TextStim(self.win, pos=[0, +10], text='use <-- and --> key for response, press "space" to confirm')

        self.resp_flag = True
        self.increment = 0

        def left_callback(event):
            self.increment = -1.0

        def right_callback(event):
            self.increment = +1.0

        def release_callback(event):
            self.increment = 0.0

        def confirm_callback(event):
            self.resp_flag = False

        def aboard_callback(event):
            self.resp_flag = False            
            self.win.close()
            core.quit()

        keyboard.on_press_key('left', left_callback)
        keyboard.on_press_key('right', right_callback)
        keyboard.on_release_key('left', release_callback)
        keyboard.on_release_key('right', release_callback)
        keyboard.hook_key('space', confirm_callback)
        keyboard.hook_key('escape', aboard_callback)

        while self.resp_flag:            
            if not self.increment == 0:                
                resp += self.increment
                resp %= 180
                prob.setOri(resp)

            message.draw()
            prob.draw()
            self.win.flip()

        keyboard.unhook_all()
        return resp

# implement io method with joy stick
class PriorLearningKeyboardJoystick(PriorLearning):
    pass
