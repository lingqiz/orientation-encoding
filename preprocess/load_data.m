function [cifti_data, motion_rg] = load_data(base_dir, ses_name)
        
data_file = fullfile(base_dir, strcat(ses_name, '_Atlas.dtseries.nii'));
motion_rg = fullfile(base_dir, strcat(ses_name, '_Movement_Regressors_dt.txt'));

% Load data
cifti_data = cifti_read(data_file);
motion_rg = load(motion_rg);

end

