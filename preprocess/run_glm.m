%% Run all GLM Fits with Filtered Data
sub_name = 'HERO_LZ';
acq_base = 'NeuralCoding%02d';
base_dir = '~/Data/fMRI';

acq_idx = {1:10, 1:9, 0:10};
base_idx = [0, 10, 19];
icafix = false;

nSes = 3;
for idx = 2:nSes
    acq_type = sprintf(acq_base, idx);
    fprintf('Run GLM for %s \n', acq_type);
    
    % save file name setup (add icafix suffix if applied)
    fl = sprintf('GLM_%s_%s', sub_name, acq_type);
    if icafix
        fl = strcat(fl, '_ICAFIX');
    end
    fl = strcat(fl, '.mat');
    
    % load data defined by ROI
    data = load_session(sub_name, acq_type, acq_idx{idx}, icafix);
    roi_mask = define_roi(sub_name);
    
    data = data(roi_mask, :);
    
    % load attention event data
    attEvent = load(fullfile(base_dir, sub_name, 'attenRT', 'atten_time.mat'));
    attEvent = attEvent.time;
    
    % Run GLM model fit
    results = glm_fit(data, attEvent, base_idx);
    
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
maskPath = '~/Desktop/Orientation_Encode/docs/all_visual_areas_mask.nii';
vareaMask = cifti_read(maskPath);
vareaMask = vareaMask.cdata;

nonVisual = 1:length(vareaMask);
nonVisual = nonVisual(~vareaMask);

fprintf('Random select out of %d non-visual voxel \n', length(nonVisual));
index = randsample(length(nonVisual), sum(roi_mask));
index = nonVisual(sort(index));
dataNonVis = data(index, :);

% Run GLM model fit on non-visual voxel
resultsNonVis = glm_fit(dataNonVis, attEvent, 0);
