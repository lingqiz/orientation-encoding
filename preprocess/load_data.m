function [cifti_data, motion_rg] = load_data(base_dir, sub_name, ses_name)

% Setup path
data_base = fullfile(base_dir, ...
            strcat(sub_name, '_', ses_name, '_', 'hcpfunc'), ...
            sub_name, 'MNINonLinear', 'Results', ses_name);
        
data_file = fullfile(data_base, strcat(ses_name, '_Atlas.dtseries.nii'));
motion_rg = fullfile(data_base, 'Movement_Regressors_dt.txt');

% Load data
cifti_data = cifti_read(data_file);
motion_rg = load(motion_rg);

end

