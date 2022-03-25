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
cifti_data = cifti_read(data_file);
motion_rg = load(motion_rg);
motion_dt = load(motion_dt);

%% Preprocessing
ts = cifti_data.cdata';

% setup nuisance variables
% decorrelation using PCA
rgs = [motion_rg, motion_dt];
[~, score, latent] = pca(rgs);

latent = latent / sum(latent);
cum_lt = cumsum(latent);

cutoff = floor(interp1(cum_lt, 1:length(cum_lt), 1-1e-5));
score = score(:, 1:cutoff);

% setup nuisance regressors
rgs = [score, ones(size(ts, 1), 1)];

% nuisance regression (normal equation)
theta = (rgs' * rgs) \ (rgs' * ts);
ts_hat = rgs * theta;

% save the residule as new time series
residule = ts - ts_hat;

%% Save output
cifti_data.cdata = residule';
data_file = fullfile(data_base, strcat(ses_name, '_Atlas.clean.dtseries.nii'));
cifti_write(cifti_data, data_file);
