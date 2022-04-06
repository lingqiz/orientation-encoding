%% Setup
function ts_filter(sub_name, acq_type, n_session)
addpath('cifti-matlab');

% sub_name: Subject label
% acq_type: Acquisition label
% n_session: Number of sessions

base_dir = strcat('~/Data/fMRI', '/', sub_name, '/', acq_type);

%% Run preprocessing for all sessions
ses_idx = 1 : n_session;

for idx = ses_idx
    % load the data file for each session
    ses_name = sprintf('func-%02d', idx);
    [cifti_data, motion_rg] = load_data(base_dir, sub_name, ses_name);

    % cifti time series
    ts = cifti_data.cdata';

    % convert to percent change
    meanVec = mean(ts, 2);
    ts = 100 * ((ts - meanVec) ./ meanVec);

    % de-trend regression
    rgs = [(1:size(ts, 1))', ones(size(ts, 1), 1)];

    % solve with normal equation
    % save the residule as new time series
    theta = (rgs' * rgs) \ (rgs' * ts);
    ts = ts - rgs * theta;

    % setup nuisance variables
    % decorrelation using PCA
    [~, score, latent] = pca(motion_rg);

    latent = latent / sum(latent);
    cum_lt = cumsum(latent);

    cutoff = ceil(interp1(cum_lt, 1:length(cum_lt), 1-1e-5));
    score = score(:, 1:cutoff);

    % setup motion nuisance regressors
    rgs = [score, ones(size(ts, 1), 1)];
    
    % solve with normal equation
    % save the residule as new time series
    theta = (rgs' * rgs) \ (rgs' * ts);
    ts = ts - rgs * theta;
    
    % save output as icafix output name
    cifti_data.cdata = ts';
    data_file = fullfile(base_dir, strcat(ses_name, '_Atlas_hp2000_clean.dtseries.nii'));
    cifti_write(cifti_data, data_file);
end

end
