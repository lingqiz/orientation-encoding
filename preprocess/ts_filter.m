%% Setup
addpath('cifti-matlab');

% Specify the subject name and data session
sub_name = 'HERO_LZ';
acq_type = 'pRF';
base_dir = strcat('~/Data/fMRI', '/', sub_name, '/', acq_type);

%% Run preprocessing for all sessions
n_session = 6;
ses_idx = 1 : n_session;

for idx = ses_idx
    % load the data file for each session
    ses_name = sprintf('func-0%d', idx);
    [cifti_data, motion_rg] = load_data(base_dir, sub_name, ses_name);
    
    % cifti time series
    ts = cifti_data.cdata';
    
    % setup nuisance variables
    % decorrelation using PCA
    [~, score, latent] = pca(motion_rg);
    
    latent = latent / sum(latent);
    cum_lt = cumsum(latent);
    
    cutoff = ceil(interp1(cum_lt, 1:length(cum_lt), 1-1e-6));
    score = score(:, 1:cutoff);
    
    % setup nuisance regressors
    rgs = [score, ones(size(ts, 1), 1)];
    
    % nuisance regression (normal equation)
    theta = (rgs' * rgs) \ (rgs' * ts);
    ts_hat = rgs * theta;
    
    % save the residule as new time series
    residule = ts - ts_hat;
    
    % save output as .clean.dtseries
    cifti_data.cdata = residule';
    data_file = fullfile(base_dir, strcat(ses_name, '_Atlas.clean.dtseries.nii'));
    cifti_write(cifti_data, data_file);
end
