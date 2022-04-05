% Simultaneous estimate of both the HRF function
% and the Beta weights of stimulus presentation

%% Load data from a single scan session
% tbUseProject('forwardModel') for setup
addpath('cifti-matlab');

% Single scan session: 91282 grayordinate * 2750 TRs (2200 sec)
% 220 sec / acquisition * 10 acquisitions
base_dir = '~/Data/fMRI';
sub_name = 'HERO_LZ';
acq_type = 'NeuralCoding01';
data_dir = fullfile(base_dir, sub_name, acq_type);

icafix_flag = false;
data = [];
if icafix_flag
    % Load icafix data
    ts_pt1 = cifti_read(fullfile(data_dir, 'ICAFIX_pt1_clean.dtseries.nii'));
    ts_pt2 = cifti_read(fullfile(data_dir, 'ICAFIX_pt2_clean.dtseries.nii'));
    data = [ts_pt1.cdata, ts_pt2.cdata];
    
else
    % Load motion regressed data
    nAcq = 10;
    base = 'func-%02d_Atlas_hp2000_clean.dtseries.nii';
    all_ts = cell(1, 10);
    for idx = 1:nAcq
        fl = sprintf(base, idx);
        ts = cifti_read(fullfile(data_dir, fl));
        all_ts{idx} = ts.cdata;
    end
    
    data = cat(2, all_ts{:});
end

%% Load eccen, varea, and r-square map
% to determine the ROI of our analysis
[eccen, varea, rsqr] = load_map(sub_name);

% V1, V2 and V3
roi_mask = (varea == 1 | varea == 2 | varea == 3);
fprintf('V1, V2, V3 # of Voxel: %d \n', sum(roi_mask));
nVoxel = sum(roi_mask);

% Apply eccentricity map
ecc_threshold = 12.0;
roi_mask  = roi_mask & (eccen > 0) & (eccen <= ecc_threshold);
fprintf('Eccen mask: %d / %d selected \n', sum(roi_mask), nVoxel);
nVoxel = sum(roi_mask);

% Apply rsquare map
r_threshold = 0.1;
roi_mask  = roi_mask & (rsqr >= r_threshold);
fprintf('Rsqur mask: %d / %d selected \n', sum(roi_mask), nVoxel);

% select voxels to analysis
data = data(roi_mask, :);

%% Set up stimulus regressors
tr = 0.8; dt = 0.5;
totalTime = 2750 * tr;

% Define a stimulus time axis with a different temporal support
stimTime = ((1:totalTime / dt) - 1) * dt;

% Single acquisition structure:
% 12.5 s * 2 blank (begin/end)
% (1.5 s Stim + 3.5 ISI) * 39 presentation
% attention event
nAcq = 10; nStim = 39;

stimDur = 1.5;
stimDly = 3.5;
blankDur = 12.5;

stim = zeros(nStim * nAcq, length(stimTime));
t = 0; stimIdx = 0;

% Calculate the time onset of each stimulus
for idx = 1:nAcq
    t = t + blankDur;
    for idy = 1:nStim
        stimIdx = stimIdx + 1;
        
        % Stim begin index
        idxStart = t / dt + 1;
        t = t + 1.5;
        % Stim end index
        idxEnd = t / dt;
        
        % Set stimulus regressor values
        stim(stimIdx, idxStart:idxEnd) = 1.0;
        t = t + 3.5;
    end
    t = t + blankDur;
end

% RT event regressor

stimTime = {stimTime'};
stimulus = {stim};

%% Run GLM model with HRF fitting
% (mtSinai model class)
results = forwardModel({data}, stimulus, tr, ...
    'modelClass', 'mtSinai', ...
    'stimTime', stimTime);
