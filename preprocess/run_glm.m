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
