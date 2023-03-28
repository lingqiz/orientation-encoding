function [tRange, meanSig] = avg_hrf(sub_name, acq_type, run_idx)
%% Setup the subject ROI index
addpath('cifti-matlab');
base_dir = strcat('~/Data/fMRI/ORNT', '/', sub_name, '/', acq_type);
[roi_mask, ~, ~] = define_roi(sub_name);

%% Setup the stimulus structure of a single acquisition
expPara = struct('acqLen', 244, 'nStim', 20, ...
    'stimDur', 1.5, 'stimDly', 10.50, 'blankDur', 4.0);

% 2 blank periods (begin/end)
% (Stim + ISI) * N stim presentation
% randomly timed attention event
nStim = expPara.nStim;
stimDur = expPara.stimDur;
stimDly = expPara.stimDly;
blankDur = expPara.blankDur;

stimTime = 1:nStim;
stimTime = (stimTime - 1) * (stimDur + stimDly) + blankDur;

%% Extract the HRF as the average stimulus invoked time course
% load the data file from a single session
ses_name = sprintf('func-%02d', run_idx);
[cifti_data, ~] = load_data(base_dir, ses_name);

ts = cifti_data.cdata';
ts = ts(:, roi_mask);

spPeriod = 0.80;
sigTime = ((1 : size(ts, 1)) - 1) * spPeriod;

% Convert to percent signal change
meanSig = mean(ts, 1);
ts = 100 * ((ts - meanSig) ./ meanSig);

% Extract time course
baseShift = 0.0;
tRange = 0 : 0.8 : (stimDur + stimDly - 0.8);
signal = zeros(nStim, length(tRange), size(ts, 2));

% get the time series
for idy = 1:nStim
    target = stimTime(idy) + baseShift + tRange;
    value = interp1(sigTime, ts, target);
    signal(idy, :, :) = value;
end

meanSig = mean(mean(signal, 3), 1);
