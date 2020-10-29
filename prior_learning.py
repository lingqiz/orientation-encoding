from psychopy import core, visual
from datetime import datetime
from sampler import sample_orientation

import numpy as np
import sys

try:
    import keyboard
except Exception as exc:    
    print('Unable to import keyboard module, keyboard IO will not be available')
    print(exc)

class DataRecord:
    def __init__(self):
        self.stimulus = []
        self.response = []
        self.react_time = []
    
    def add_stimulus(self, stim):
        self.stimulus.append(stim)
    
    def add_response(self, resp):
        self.response.append(resp)

    def add_react_time(self, time):
        self.react_time.append(time)

    def to_numpy(self):
        n_trial = len(self.stimulus)

        data_mtx = np.zeros([3, n_trial])
        data_mtx[0, :] = self.stimulus
        data_mtx[1, :] = self.response
        data_mtx[2, :] = self.react_time

        return data_mtx

class PriorLearning:
    '''base class for our prior learning experiment'''
    def __init__(self, n_trial, uniform=True, show_fb=False):
        # subject name/id
        self.sub_val = input("enter subject name/ID: ")

        # will be used for recording response
        self.resp_flag = True
        self.increment = 0

        # parameter for the experiment
        self.n_trial = n_trial
        self.uniform = uniform
        self.show_fb = show_fb
        
        # initialize window, message
        self.win = visual.Window(size=(1920, 1080), fullscr=True, allowGUI=True, monitor='testMonitor', units='deg')
        self.welcome = visual.TextStim(self.win, pos=[0,-5], text='Thanks for your time. Press "space" to continue.')
        self.inst1 = visual.TextStim(self.win, pos=[0,+5], text='You will first see a quickly flashed gabor stimulus.')
        self.inst2 = visual.TextStim(self.win, pos=[0,0], text='After the stimulus, adjust the prob using <-- and --> to match its orientation.')

        # initialize stimulus
        self.target = visual.GratingStim(self.win, sf=0.5, size=6.0, mask='gauss', contrast=0.10)
        self.fixation = visual.GratingStim(self.win, color=-1, colorSpace='rgb', tex=None, mask='circle', size=0.2)
        self.feedback = visual.Line(self.win, start=(0.0, -2.0), end=(0.0, 2.0), lineWidth=5.0, lineColor='black', size=1, contrast=0.80)

        return

    def start(self):        
        # show welcome message and instruction
        self.welcome.draw()
        self.inst1.draw()
        self.inst2.draw()
        self.win.flip()

        self.io_wait()
        self.record = DataRecord()

        return

    def run(self):
        for idx in range(self.n_trial):
            # ISI for 1.0 s
            self.fixation.draw()
            self.win.flip()
            core.wait(1.0)
            
            # Draw stimulus for 200 ms
            # Sample from an orientation distribution (uniform/natural)
            targetOri = sample_orientation(n_sample=1, uniform=self.uniform)
            targetOri = float(targetOri)
            self.record.add_stimulus(targetOri)
            
            self.target.setOri(targetOri)
            self.target.draw()
            self.fixation.draw()
            self.win.flip()
            core.wait(0.2)

            # blank screen for 2s            
            self.win.flip()
            core.wait(2.0)

            # record response
            clock = core.Clock()
            response = self.io_response()

            self.record.add_response(response)
            self.record.add_react_time(clock.getTime())

            # feedback for 1s
            if self.show_fb:
                self.feedback.setOri(response)

                self.target.draw()
                self.feedback.draw()
                self.win.flip()
                core.wait(1.0)

        return

    def end(self):
        # write data as both .CSV and .NPY file
        data_mtx = self.record.to_numpy()

        time = datetime.now()
        dt_string = time.strftime("%d_%m_%Y_%H_%M_")
        file_name = dt_string + self.sub_val

        np.savetxt(file_name + '.csv', data_mtx, delimiter=",")
        np.save(file_name + '.npy', data_mtx)

        return
    
    def pause(self):
        pause_msg = visual.TextStim(self.win, pos=[0, 0], text='Take a short break. Press "space" when you are ready to continue.')
        pause_msg.draw()
        self.win.flip()
        self.io_wait()

        return

    def io_wait(self):
        raise NotImplementedError("IO Method not implemented in the base class")
    
    def io_response(self):
        raise NotImplementedError("IO Method not implemented in the base class")

# implement io method with keyboard
class PriorLearningKeyboard(PriorLearning):
    
    def io_wait(self):
        '''override io_wait'''
        keyboard.wait('space')
        return
    
    def io_response(self):
        '''override io_response'''
        resp = int(sample_orientation(n_sample=1, uniform=True))

        prob = visual.Line(self.win, start=(0.0, -2.0), end=(0.0, 2.0), lineWidth=5.0, lineColor='black', size=1, ori=resp, contrast=0.80)
        message = visual.TextStim(self.win, pos=[0, +10], text='use <-- and --> key for response, press "space" to confirm')

        # global variable for recording response
        self.resp_flag = True
        self.increment = 0

        # define callback function for keyboard event
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

        # key binding for recording response
        key_bind = {'left':left_callback, 'right':right_callback, 'space':confirm_callback, 'escape':aboard_callback}
        for key, callback in key_bind.items():
            keyboard.on_press_key(key, callback)

        for key in ['left', 'right']:
            keyboard.on_release_key(key, release_callback)                

        # wait/record for response
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

# TODO: implement io method with joy stick
class PriorLearningKeyboardJoystick(PriorLearning):
    pass
