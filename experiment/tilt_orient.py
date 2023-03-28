from psychopy import core, visual
from datetime import datetime
from .sampler import sample_orientation
import os, json, random, numpy as np

# for keyboard IO
try:
    import keyboard

except Exception as exc:
    print(exc)
    print('Unable to import keyboard module, \
            keyboard IO will not be available')

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

    def to_numpy(self):
        n_trial = len(self.stimulus)
        data_mtx = np.zeros([2, n_trial])

        data_mtx[0, :] = self.surround
        data_mtx[1, :] = self.stimulus

        return data_mtx

class OrientEncode:

    # default parameters for the experiment
    DEFAULT_DUR = 1.5
    DEFAULT_BLANK = 4.0
    DEFAULT_DELAY = 4.5
    DEFAULT_RESP = 4.0
    DEFAULT_ISI = 2.0
    DEFAULT_LEN = 5.0

    # conditions of the experiment
    N_COND = 3
    N_SESSION = 20
    N_TRIAL = 20
    SURROUND_VAL = [-1, 35.0, 145.0]

    def __init__(self, sub_val):
        # subject name/id
        self.sub_val = sub_val
        self.time_stmp = datetime.now().strftime("%d_%m_%Y_%H_%M_")

        # set parameter for the experiment
        self.n_trial = self.N_TRIAL
        self.line_len = self.DEFAULT_LEN
        self.stim_dur = self.DEFAULT_DUR
        self.blank = self.DEFAULT_BLANK
        self.delay = self.DEFAULT_DELAY
        self.resp_dur = self.DEFAULT_RESP
        self.isi = self.DEFAULT_ISI

        # create condition sequence / record file for each subject
        self.data_dir = os.path.join('.', 'Neural', self.sub_val)
        self.record_path = os.path.join(self.data_dir, self.sub_val + '.json')

        if os.path.exists(self.record_path):
            with open(self.record_path, 'r') as file_handle:
                self.sub_record = json.load(file_handle)
        else:
            os.mkdir(self.data_dir)

            # sample stimulus to present
            # using stratified sampling over [0, 1] to ensure uniformity
            stim_seq = []
            for _ in range(self.N_COND):
                edges = np.linspace(0, 1, self.n_trial * self.N_SESSION + 1)
                samples = np.array([np.random.uniform(edges[idx], edges[idx+1])
                                for idx in range(self.n_trial * self.N_SESSION)]) * 180.0
                np.random.shuffle(samples)
                stim_seq.extend(samples.astype(np.int).tolist())

            # sequence of conditions
            cond = []
            for _ in range(self.N_SESSION):
                cond_idx = [0, 1, 2]
                random.shuffle(cond_idx)
                cond.extend(cond_idx)

            # create subject record and save initial json file
            self.sub_record = {'Cond_List' : cond,
                               'Ses_Counter' : 0,
                               'Cond_Counter' : [0, 0, 0],
                               'Stim_Seq' : stim_seq,
                               'Resp_Seq' : []}

            self._save_json()
            print('create subject file at ' + self.record_path)

        # will be used for recording response
        self.resp_flag = True
        self.increment = 0

        # get the stimulus sequence
        self.run_idx = self.sub_record['Ses_Counter']
        self.cond_idx = self.sub_record['Cond_List'][self.run_idx]

        all_stims = np.reshape(np.array(self.sub_record['Stim_Seq']), (self.N_COND, -1))
        stim_seq = np.reshape(all_stims[self.cond_idx, :], (self.N_SESSION, self.n_trial))
        self.stim_seq = stim_seq[self.sub_record['Cond_Counter'][self.cond_idx], :]

        # initialize window, message
        # monitor = 'rm_413' for psychophysics and 'sc_3t' for imaging session
        self.win = visual.Window(size=(1920, 1080), fullscr=True, allowGUI=True, screen=1, monitor='sc_3t', units='deg', winType=window_backend)

        # initialize stimulus
        self.target = visual.GratingStim(self.win, sf=1.0, size=10.0, mask='raisedCos', maskParams={'fringeWidth':0.25}, contrast=0.20)
        self.noise = visual.NoiseStim(self.win, units='pix', mask='raisedCos', size=1024, contrast=0.10, noiseClip=3.0,
                                    noiseType='Filtered', texRes=1024, noiseElementSize=4, noiseFractalPower=0,
                                    noiseFilterLower=15.0/1024.0, noiseFilterUpper=25.0/1024.0, noiseFilterOrder=3.0)
        self.surround = visual.GratingStim(self.win, sf=1.0, size=18.0, mask='raisedCos', contrast=0.10)
        self.surround.ori = self.SURROUND_VAL[self.cond_idx]

        self.fixation = visual.GratingStim(self.win, color=0.5, colorSpace='rgb', tex=None, mask='raisedCos', size=0.25)
        self.center = visual.GratingStim(self.win, sf=0.0, size=2.0, mask='raisedCos', maskParams={'fringeWidth':0.15}, contrast=0.0)
        self.prob = visual.Line(self.win, start=(0.0, -self.line_len), end=(0.0, self.line_len), lineWidth=10.0, lineColor='black', size=1, contrast=0.80)

        return

    def _save_json(self):
        with open(self.record_path, 'w+') as record:
            record.write(json.dumps(self.sub_record, indent=2))
        return

    def _draw_blank(self):
        self.fixation.draw()
        self.win.flip()

        return

    def start(self):
        # determine condition and sequence
        print('Acquisition Total Run #%d' % self.run_idx)
        print('Surround Cond %d, Run #%d' % (self.cond_idx,
            self.sub_record['Cond_Counter'][self.cond_idx]))

        self.sub_record['Ses_Counter'] += 1
        self.sub_record['Cond_Counter'][self.cond_idx] += 1

        # set up for the first trial
        self.target.ori = self.stim_seq[0]
        self.target.phase = np.random.rand()

        # wait for scanner signal
        self.io_wait(wait_key='T')

        return

    def run(self):
        '''
        Experiment parameters:
            4.0s * 1 blank (beginning)
            20 trial * (1.5s stim + 10.5s delay)
            244s total, 244/0.8 = 305 TRs
        '''
        # start experiment
        # clock for global and trial timing
        self.global_clock = core.Clock()
        self.global_ctd = core.Clock()

        # initial blank period
        self.global_ctd.add(self.blank)
        while self.global_ctd.getTime () <= 0:
            self._draw_blank()

        for idx in range(self.n_trial):
            # draw stimulus for a fixed duration
            self.global_ctd.add(self.stim_dur)
            while self.global_ctd.getTime() <= 0:
                # 2 hz contrast modulation
                t = self.global_ctd.getTime() + self.stim_dur
                crst = 0.10 * np.cos(4.0 * np.pi * t + np.pi) + 0.10

                if self.cond_idx == 0:
                    # draw noise surround
                    self.noise.contrast = crst
                    self.noise.draw()
                else:
                    # draw oriented surround
                    self.surround.contrast = crst
                    self.surround.draw()

                self.target.contrast = crst
                self.target.draw()
                self.center.draw()

                # draw fixation dot
                self.fixation.draw()
                self.win.flip()

            # slight jitter (+/- 0.5 sec) in delay period
            delta = np.random.uniform(0, 1) - 0.5

            # blank screen for delay duration
            # also set up the next stim
            self.global_ctd.add(self.delay + delta)

            # setup stim condition for next trial
            if idx < self.n_trial - 1:
                self.target.ori = self.stim_seq[idx + 1]
                self.target.phase = np.random.rand()

                # update surround
                if self.cond_idx == 0:
                    self.noise.updateNoise()
                else:
                    self.surround.phase = np.random.rand()

            # blank period
            while self.global_ctd.getTime() <= 0:
                self._draw_blank()

            # response period
            resp_dur = self.resp_dur - delta
            self.global_ctd.add(resp_dur)
            response = self.io_response(resp_dur)
            self.sub_record['Resp_Seq'].append(int(response))

            # ISI
            self.global_ctd.add(self.isi)
            while self.global_ctd.getTime() <= 0:
                self._draw_blank()

        # record session time
        self.session_time = self.global_clock.getTime()

        return

    def save_data(self):
        # write subject record
        self._save_json()

        return

    def pause(self):
        self.save_data()
        self.io_wait(wait_key='space')
        return

    def end(self):
        self.save_data()
        print('Successfully finish the experiment!')

    def io_wait(self):
        raise NotImplementedError("IO Method not implemented in the base class")

    def io_response(self, dur):
        raise NotImplementedError("IO Method not implemented in the base class")

# Implement IO method with keyboard
class OrientEncodeKeyboard(OrientEncode):

    def io_wait(self, wait_key='space'):
        '''override io_wait'''
        self.resp_flag = True
        def confirm_callback(event):
            self.resp_flag= False

        # register callback, wait for key press
        keyboard.on_release_key(wait_key, confirm_callback)
        while self.resp_flag:
            self.win.flip()

        keyboard.unhook_all()
        return

    def io_response(self, dur):
        '''override io_response'''
        resp = int(sample_orientation(n_sample=1, uniform=True))
        self.prob.setOri(resp)

        # global variable for recording response
        self.increment = 0

        # define callback function for keyboard event
        def left_callback(event):
            self.increment = -1.0

        def right_callback(event):
            self.increment = +1.0

        def release_callback(event):
            self.increment = 0.0

        # key binding for recording response
        key_bind = {'B':left_callback, 'Y':right_callback}
        for key, callback in key_bind.items():
            keyboard.on_press_key(key, callback)

        for key in ['B', 'Y']:
            keyboard.on_release_key(key, release_callback)

        # wait/record for response
        while self.global_ctd.getTime() <= 0:
            t = self.global_ctd.getTime()
            self.prob.contrast = np.abs(t / dur * 0.75)

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
class OrientEncodeButtons(OrientEncode):

    def __init__(self, sub_val, n_trial, mode='uniform', show_fb=False, joy_id=0):
        super(OrientEncodeButtons, self).__init__(sub_val, n_trial, mode, show_fb)
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

    def io_response(self, dur):
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
class OrientEncodeJoystick(OrientEncodeButtons):
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