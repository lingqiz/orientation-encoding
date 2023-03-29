%% Run GLM model with a new design (Code ORNT)
% TO-DO: change data loading to be compatible with the new version
sub_name = 'HERO_JM';
acq_base = 'NeuralCoding%02d';
base_dir = '~/Data/fMRI';

nAcq = 10;
acq_idx = {1:nAcq};
base_idx = 0;
icafix = false;
modelClass = 'glm';

% Setup the structure of a single acquisition (check Python file)
expPara = struct('acqLen', 244, 'nStim', 20, ...
    'stimDur', 1.5, 'stimDly', 10.50, 'blankDur', 4.0);

% Session: NeuralCoding01 / 02
idx = 1;
ses_idx = 1;

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
plotIdx = 1:9;
subplot(1, 10, plotIdx);
xlim([0, expPara.acqLen * nAcq]);

% add the varea label and eccentricity label to results struct
results.v_label = v_label;
results.e_label = e_label;

% save results
fl_path = fullfile(base_dir, sub_name, fl);
save(fl_path, 'results', 'roi_mask', 'sub_name', 'acq_type');
