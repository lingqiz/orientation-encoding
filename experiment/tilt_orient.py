from psychopy import core, visual
from datetime import datetime
from .sampler import sample_orientation, sample_stimuli
from random import shuffle
from numpy.core.numeric import NaN
import os, numpy as np

# for keyboard IO
try:
    import keyboard
except Exception as exc:
    print('Unable to import keyboard module, keyboard IO will not be available')
    print(exc)

# for joystick IO
# 'glfw' or 'pyglet' for backend
window_backend = 'glfw'
from psychopy.hardware import joystick
joystick.backend = window_backend

# simple class for experiment data
class DataRecord:
    def __init__(self):
        self.surround = []
        self.stimulus = []
        self.response = []
        self.react_time = []

    def add_surround(self, surround):
        self.surround.append(surround)

    def add_stimulus(self, stim):
        self.stimulus.append(stim)

    def add_response(self, resp):
        self.response.append(resp)

    def add_react_time(self, time):
        self.react_time.append(time)

    def to_numpy(self, record_resp):
        n_trial = len(self.stimulus)
        data_mtx = np.zeros([4, n_trial])

        data_mtx[0, :] = self.surround
        data_mtx[1, :] = self.stimulus

        if record_resp:
            data_mtx[2, :] = self.response
            data_mtx[3, :] = self.react_time

        return data_mtx

class PriorLearning:

    # static variable for the surround conditions (SF, Ori)
    COND = [(NaN, NaN), (0.5, 30), (0.5, 150)]

    def __init__(self, sub_val, n_trial, mode='uniform', show_fb=False, record_resp=True, atten_task=False, record_sc=False):
        # subject name/id
        self.sub_val = sub_val
        self.time_stmp = datetime.now().strftime("%d_%m_%Y_%H_%M_")

        # will be used for recording response
        self.resp_flag = True
        self.increment = 0

        # parameter for the experiment
        self.n_trial = n_trial
        self.mode = mode
        self.show_fb = show_fb
        self.line_len = 3.0
        self.record_resp = record_resp
        self.atten_task = atten_task
        self.record_sc = record_sc

        self.stim_dur = 1.5
        self.delay = 4.5

        # initialize window, message
        # monitor = 'testMonitor' or 'rm_413'
        self.win = visual.Window(size=(1920, 1080), fullscr=True, allowGUI=True, monitor='rm_413', units='deg', winType=window_backend)
        self.welcome = visual.TextStim(self.win, pos=[0,-5], text='Thanks for your time. Press "space" to continue.')
        self.inst1 = visual.TextStim(self.win, pos=[0,+5], text='You will first see a quickly flashed gabor stimulus.')
        self.inst2 = visual.TextStim(self.win, pos=[0,0], text='After the stimulus, adjust the prob using L1 and R1 to match its orientation.')
        self.pause_msg = visual.TextStim(self.win, pos=[0, 0], text='Take a short break. Press "space" when you are ready to continue.')

        # initialize stimulus
        self.target = visual.GratingStim(self.win, sf=0.50, size=10.0, mask='raisedCos', maskParams={'fringeWidth':0.25}, contrast=0.10)
        self.surround = visual.GratingStim(self.win, sf=0.50, size=18.0, mask='raisedCos', contrast=0.10)
        self.noise = visual.NoiseStim(self.win, units='pix', mask='raisedCos', size=1024, contrast=0.10, noiseClip=3.0,
                                    noiseType='Filtered', texRes=1024, noiseElementSize=4, noiseFractalPower=0,
                                    noiseFilterLower=7.5/1024.0, noiseFilterUpper=12.5/1024.0, noiseFilterOrder=3.0)

        self.fixation = visual.GratingStim(self.win, color=0.5, colorSpace='rgb', tex=None, mask='circle', size=0.2)
        self.feedback = visual.Line(self.win, start=(0.0, -self.line_len), end=(0.0, self.line_len), lineWidth=5.0, lineColor='black', size=1, contrast=0.80)
        self.prob = visual.GratingStim(self.win, sf=0.5, size=[2.0, 5.0], mask='gauss', contrast=1.0)

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
        # create a of conditions and stimulus
        stim_list = []
        n_sample = int(self.n_trial // len(self.COND))
        for cond_idx in range(len(self.COND)):
            samples = sample_stimuli(n_sample, mode='uniform')
            stim_list += list(zip([cond_idx] * n_sample, samples))
        shuffle(stim_list)

        # start experiment
        # start a clock
        clock = core.Clock()
        for idx in range(self.n_trial):
            # ISI for 1.0 s
            self.fixation.draw()
            self.win.flip()
            core.wait(1.0)

            # draw stimulus for 250 ms
            # surround orientation
            surround = None
            cond_idx, stim_ori = stim_list[idx]
            if np.isnan(self.COND[cond_idx][0]):
                self.record.add_surround(NaN)
                self.noise.updateNoise()
                surround = self.noise
            else:
                self.record.add_surround(self.COND[cond_idx][1])
                self.surround.sf, self.surround.ori = self.COND[cond_idx]
                surround = self.surround

            # center orientation
            self.record.add_stimulus(stim_ori)
            self.target.setOri(stim_ori)

            clock.reset()
            while clock.getTime() <= self.stim_dur:
                # 2 hz contrast modulation
                crst = 0.05 * np.cos(4.0 * np.pi * clock.getTime() + np.pi) + 0.05
                # draw stim
                surround.contrast = crst
                surround.draw()

                self.target.contrast = crst
                self.target.draw()

                # draw fixation dot
                self.fixation.draw()
                self.win.flip()

            if self.record_sc:
                self.win.getMovieFrame()

            # blank screen for delay duration
            clock.reset()
            while clock.getTime() <= self.delay:
                self.fixation.draw()
                self.win.flip()

            # record response
            if self.record_resp and (not self.record_sc):
                clock.reset()
                response = self.io_response()

                self.record.add_response(response)
                self.record.add_react_time(clock.getTime())

        return

    def save_data(self):
        file_name = self.time_stmp + self.sub_val

        if self.record_sc:
            self.win.saveMovieFrames(os.path.join('.', 'Record', file_name + '.tif'))

        else:
            # write data as both .CSV and .NPY file
            data_mtx = self.record.to_numpy(self.record_resp)

            np.savetxt(file_name + '.csv', data_mtx, delimiter=",")
            np.save(file_name + '.npy', data_mtx)

        return

    def pause(self):
        self.pause_msg.draw()
        self.win.flip()
        self.io_wait()

        return

    def end(self):
        self.save_data()
        print('Successfully finish the experiment!')

    def io_wait(self):
        raise NotImplementedError("IO Method not implemented in the base class")

    def io_response(self):
        raise NotImplementedError("IO Method not implemented in the base class")

# Implement IO method with keyboard
class PriorLearningKeyboard(PriorLearning):

    def io_wait(self):
        '''override io_wait'''
        keyboard.wait('space')
        return

    def io_response(self):
        '''override io_response'''
        resp = int(sample_orientation(n_sample=1, uniform=True))
        self.prob.setOri(resp)

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
                self.prob.setOri(resp)

            self.prob.draw()
            self.fixation.draw()
            self.win.flip()

        keyboard.unhook_all()
        return resp

# IO with joystick button push
class PriorLearningButtons(PriorLearning):

    def __init__(self, sub_val, n_trial, mode='uniform', show_fb=False, joy_id=0):
        super(PriorLearningButtons, self).__init__(sub_val, n_trial, mode, show_fb)
        self.L1 = 4
        self.L2 = 6
        self.R1 = 5
        self.R2 = 7

        self.welcome = visual.TextStim(self.win, pos=[0,-5], text='Thanks for your time. Press L2 or R2 to continue.')
        self.pause_msg = visual.TextStim(self.win, pos=[0, 0], text='Take a short break. Press L2 or R2 when you are ready to continue.')

        nJoys = joystick.getNumJoysticks()
        if nJoys < joy_id:
            print('Joystick Not Found')

        self.joy = joystick.Joystick(joy_id)

    def start(self):
        while not self.confirm_press():
            self.welcome.draw()
            self.inst1.draw()
            self.inst2.draw()
            self.win.flip()

        self.record = DataRecord()

    def pause(self):
        core.wait(0.5)
        self.win.flip()
        while not self.confirm_press():
            self.pause_msg.draw()
            self.win.flip()

    # override start and pause so io_wait is not required anymore
    def io_wait(self):
        '''override io_wait'''
        return

    def io_response(self):
        '''override io_response'''
        resp = int(sample_orientation(n_sample=1, uniform=True))
        self.prob.setOri(resp)

        while not self.confirm_press():
            self.prob.draw()
            self.fixation.draw()
            self.win.flip()

            if self.joy.getButton(self.L1):
                resp -= 1
                resp %= 180
                self.prob.setOri(resp)

            if self.joy.getButton(self.R1):
                resp += 1
                resp %= 180
                self.prob.setOri(resp)

        return resp

    def confirm_press(self):
        return self.joy.getButton(self.L2) or \
                self.joy.getButton(self.R2)

# Response with Joystick Axis
class PriorLearningJoystick(PriorLearningButtons):
    def io_response(self):
        '''override io_response'''
        resp = int(sample_orientation(n_sample=1, uniform=True))
        self.prob.setOri(resp)

        while not self.confirm_press():
            self.prob.draw()
            self.fixation.draw()
            self.win.flip()

            x = self.joy.getX()
            y = self.joy.getY()
            if np.sqrt(x ** 2 + y ** 2) >= 1:
                resp = (np.arctan(y / x) / np.pi * 180.0 - 90) % 180
                self.prob.setOri(resp)

        return resp

    # use different buttons to confirm response
    def confirm_press(self):
        return self.joy.getButton(self.L1) or \
                self.joy.getButton(self.R1)