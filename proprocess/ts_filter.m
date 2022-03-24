%% Setup
addpath('cifti-matlab');

sub_name = 'HERO_LZ';
ses_name = 'func-01';
base_dir = '~/Data/fMRI';

% path to the data file
data_base = fullfile(base_dir, ...
            strcat(sub_name, '_', ses_name, '_', 'hcpfunc'), ...
            sub_name, 'MNINonLinear', 'Results', ses_name);
        
data_file = fullfile(data_base, strcat(ses_name, '_Atlas.dtseries.nii'));
motion_rg = fullfile(data_base, 'Movement_Regressors.txt');
motion_dt = fullfile(data_base, 'Movement_Regressors_dt.txt');

% Load data
data = cifti_read(data_file);
motion_rg = load(motion_rg);
motion_dt = load(motion_dt);

%% Preprocessing
ts = data.cdata';

% nuisance variables
t_index = 1:420;
rgs = [motion_rg, motion_dt];
[~, score, latent] = pca(rgs);

latent = latent / sum(latent);
cum_lt = cumsum(latent);

cutoff = floor(interp1(cum_lt, 1:length(cum_lt), 1-1e-5));

% nuisance regression
% theta = (rgs' * rgs) \ (rgs' * ts);