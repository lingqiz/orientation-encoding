%% Run all GLM Fits with Filtered Data
sub_name = 'HERO_LZ';
acq_base = 'NeuralCoding%02d';
base_dir = '~/Data/fMRI';

acq_idx = {1:10, 1:9, 0:10};
base_idx = [0, 10, 19];
icafix = false;
modelClass = 'glm';

% Setup the structure of a single acquisition
expPara = struct('acqLen', 220, 'nStim', 39, ...
    'stimDur', 1.5, 'stimDly', 3.5, 'blankDur', 12.5);

nSes = 3;
for idx = 1 : nSes
    acq_type = sprintf(acq_base, idx);
    fprintf('Run %s fitting for %s \n', modelClass, acq_type);
    
    % save file name setup (add icafix suffix if applied)
    fl = sprintf('%s_%s_%s', modelClass, sub_name, acq_type);
    if icafix
        fl = strcat(fl, '_ICAFIX');
    end
    fl = strcat(fl, '.mat');
    
    % load data defined by ROI
    data = load_session(sub_name, acq_type, acq_idx{idx}, icafix);
    [roi_mask, v_label, e_label] = define_roi(sub_name);
    
    data = data(roi_mask, :);
    
    % load attention event data
    attEvent = load(fullfile(base_dir, sub_name, 'attenRT', 'atten_time.mat'));
    attEvent = attEvent.time;
    
    % Run GLM model fit
    results = glm_fit(data, expPara, attEvent, base_idx(idx), ...
            'showPlot', true, 'modelClass', modelClass);
    
    % add the varea label and eccentricity label to results struct
    results.v_label = v_label;
    results.e_label = e_label;
    
    % save results
    fl_path = fullfile(base_dir, sub_name, fl);
    save(fl_path, 'results', 'roi_mask', 'sub_name', 'acq_type');
end

%% Run GLM on a "null" distribution
sub_name = 'HERO_LZ';
acq_type = 'NeuralCoding01';
base_dir = '~/Data/fMRI';
acq_idx = 1:10;

% Load data
data = load_session(sub_name, acq_type, acq_idx, false);
roi_mask = define_roi(sub_name);

% Generate Gaussian white noise as "null" data
dataNull = normrnd(0, 1, size(data(roi_mask, :)));

% load attention event data
attEvent = load(fullfile(base_dir, sub_name, 'attenRT', 'atten_time.mat'));
attEvent = attEvent.time;

% Run GLM model fit on null data
resultsNull = glm_fit(dataNull, attEvent, 0);

%% Run GLM on non-visual area
[~, varea, ~] = load_map(sub_name);
nonVisual = 1:length(varea);
nonVisual = nonVisual(varea == 0);

index = randsample(length(nonVisual), sum(roi_mask));
index = nonVisual(sort(index));

fprintf('Random select %d out of %d non-visual voxel \n', ...
        length(index), length(nonVisual));
    
dataNonVis = data(index, :);

% Run GLM model fit on non-visual voxel
resultsNonVis = glm_fit(dataNonVis, attEvent, 0);

%% Run GLM model with a new design (Sept 2022)
sub_name = 'HERO_JM';
acq_base = 'NeuralCoding%02d';
base_dir = '~/Data/fMRI';

acq_idx = {1:10};
base_idx = 0;
icafix = false;
modelClass = 'mtSinai';

% Setup the structure of a single acquisition
expPara = struct('acqLen', 320, 'nStim', 39, ...
    'stimDur', 1.5, 'stimDly', 6.0, 'blankDur', 13.75);

% Session: NeuralCoding00
idx = 1;
ses_idx = 0;

acq_type = sprintf(acq_base, ses_idx);
fprintf('Run %s fitting for %s \n', modelClass, acq_type);

% save file name setup (add icafix suffix if applied)
fl = sprintf('%s_%s_%s', modelClass, sub_name, acq_type);
if icafix
    fl = strcat(fl, '_ICAFIX');
end
fl = strcat(fl, '.mat');

% load data defined by ROI
data = load_session(sub_name, acq_type, acq_idx{idx}, icafix);
[roi_mask, v_label, e_label] = define_roi(sub_name);

data = data(roi_mask, :);

% load attention event data
attEvent = load(fullfile(base_dir, sub_name, 'attenRT', 'atten_time.mat'));
attEvent = attEvent.time;

% Run GLM model fit
results = glm_fit(data, expPara, attEvent, base_idx(idx), ...
    'showPlot', true, 'modelClass', modelClass);

% add the varea label and eccentricity label to results struct
results.v_label = v_label;
results.e_label = e_label;

% save results
fl_path = fullfile(base_dir, sub_name, fl);
save(fl_path, 'results', 'roi_mask', 'sub_name', 'acq_type');

%% Run GLM model with a new design (Oct 2022)
sub_name = 'HERO_TW';
acq_base = 'NeuralCoding%02d';
base_dir = '~/Data/fMRI';

nAcq = 10;
acq_idx = {1:nAcq};
base_idx = 0;
icafix = false;
modelClass = 'glm';

% Setup the structure of a single acquisition
expPara = struct('acqLen', 252, 'nStim', 20, ...
    'stimDur', 1.5, 'stimDly', 10.50, 'blankDur', 12.0);

% Session: NeuralCoding00
idx = 1;
ses_idx = 0;

acq_type = sprintf(acq_base, ses_idx);
fprintf('Run %s fitting for %s \n', modelClass, acq_type);

% save file name setup (add icafix suffix if applied)
fl = strcat(sprintf('%s_%s_%s', modelClass, sub_name, acq_type), '.mat');

% load data defined by ROI
data = load_session(sub_name, acq_type, acq_idx{idx}, icafix);
[roi_mask, v_label, e_label] = define_roi(sub_name);

data = data(roi_mask, :);

% Run GLM model fit
results = glm_fit(data, expPara, [], base_idx(idx), ...
    'showPlot', true, 'modelClass', modelClass);

figure(2);
subplot(1, 10, 1:9);
xlim([0, expPara.acqLen * nAcq]);

% add the varea label and eccentricity label to results struct
results.v_label = v_label;
results.e_label = e_label;

% save results
fl_path = fullfile(base_dir, sub_name, fl);
save(fl_path, 'results', 'roi_mask', 'sub_name', 'acq_type');
