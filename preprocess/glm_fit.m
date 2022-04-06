function glm_fit(sub_name, acq_type, acq_idx, base_idx)

%% Load data from a single scan session
% tbUseProject('forwardModel') for setup
addpath('cifti-matlab');

% Single scan session: 91282 grayordinate * nAcq * 275 TRs
% 220 sec / acquisition * n acquisitions
base_dir = '~/Data/fMRI';
data_dir = fullfile(base_dir, sub_name, acq_type);

% Load motion regressed data
base = 'func-%02d_Atlas_hp2000_clean.dtseries.nii';
all_ts = cell(1, 10);
for idx = acq_idx
    fl = sprintf(base, idx);
    ts = cifti_read(fullfile(data_dir, fl));
    all_ts{idx} = ts.cdata;
end

data = cat(2, all_ts{:});

%% Load eccen, varea, and r-square map
% to determine the ROI of our analysis
[eccen, varea, rsqr] = load_map(sub_name);

% V1, V2 and V3
roi_mask = (varea == 1 | varea == 2 | varea == 3);
fprintf('V1, V2, V3 # of Voxel: %d \n', sum(roi_mask));
nVoxel = sum(roi_mask);

% Apply eccentricity map
ecc_threshold = 15.0;
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
totalTime = size(data, 2) * tr;

acqLen = 220.0;
nAcq = totalTime / acqLen;

% Define a stimulus time axis with a different temporal support
stimTime = ((1:totalTime / dt) - 1) * dt;

% Single acquisition structure:
% 12.5 s * 2 blank (begin/end)
% (1.5 s Stim + 3.5 ISI) * 39 presentation
% attention event
nStim = 39;

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

%% Set up attent event regressor
attEvent = load(fullfile(base_dir, sub_name, 'attenRT', 'atten_time.mat'));
attEvent = attEvent.time;

% Plot attention RT
figure();
allRT = cat(1, attEvent{:});
histogram(allRT(:, 2)); box off;
xlabel('Time'); ylabel('Count');

baseIdx = base_idx;
eventRegressor = zeros(1, length(stimTime));

for idx = 1:nAcq
    baseTime = (idx - 1) * acqLen;
    event = attEvent{baseIdx + idx};
    eventTime = baseTime + event(:, 1);
    
    for et = eventTime
        idxStart = ceil(et / dt) + 1;
        eventRegressor(idxStart) = 1.0;
    end
end

stim = [stim; eventRegressor];

%% Run GLM model with HRF fitting (mtSinai model class)
% polynom low freq noise removal 
modelOpts = {'polyDeg', 4};
results = forwardModel({data}, {stim}, tr, ...
                  'modelClass', 'mtSinai', ...
                  'stimTime', {stimTime'}, ...
                  'modelOpts', modelOpts);

fl = sprintf('GLM_%s_%s.mat', sub_name, acq_type);
fl_path = fullfile(base_dir, sub_name, fl);
save(fl_path, 'results', 'roi_mask', 'sub_name', 'acq_type');

%% Post model fitting checks
figure();
histogram(results.R2); box off;
xlabel('R2'); ylabel('Count');

% Show the results figures
figFields = fieldnames(results.figures);
if ~isempty(figFields)
    for ii = 1:length(figFields)
        figHandle = struct2handle(results.figures.(figFields{ii}).hgS_070000,0,'convert');
        set(figHandle,'visible','on')
    end
end

end
