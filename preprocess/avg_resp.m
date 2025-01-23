function avg_resp(sub_name, acq_type, n_session, varargin)
addpath('cifti-matlab');

%% Required rarameters
% sub_name: Subject label
% acq_type: Acquisition label
% n_session: Number of sessions

%% Optional parameters
% Define ROI: visual area index and eccentricity
% Stimulus: 0 - 1.5 deg; 1.5 - 7 deg; > 7 deg

% Area - Index Correspondence
% {1:  'V1',   2: 'V2',  3: 'V3',  4: 'hV4',  5: 'VO1', 6:  'VO2',  
% 7: 'LO1', 8: 'LO2', 9: 'TO1', 10: 'TO2', 11: 'V3b', 12: 'V3a'}

%% Extract "beta" response from voxel time series
p = inputParser;

% Default ROI: V1 - V3 area, foeval - 7.0 degree eccentricity
p.addParameter('areaIndex', [1, 2, 3]);
p.addParameter('eccLo', 1.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('eccHi', 7.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('polarLo', 0.0);
p.addParameter('polarHi', 0.0);
p.addParameter('nonVisual', 0);
p.addParameter('prfROI', 0);
p.addParameter('cutoffT', 150, @(x)(isnumeric(x) && numel(x) == 1))
p.addParameter('saveDir', '');

parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccLo = p.Results.eccLo;
eccHi = p.Results.eccHi;
polarLo = p.Results.polarLo;
polarHi = p.Results.polarHi;
nonVisual = p.Results.nonVisual;
prfROI = p.Results.prfROI;
cutOffT = p.Results.cutoffT;
saveDir = p.Results.saveDir;

% Define ROI
[roi_mask, v_label, e_label] = define_roi(sub_name, 'areaIndex', areaIndex, ...
                                        'eccLo', eccLo, 'eccHi', eccHi, ...
                                        'nonVisual', nonVisual, 'prfROI', prfROI, ...
                                        'polarLo', polarLo, 'polarHi', polarHi);

% Setup the time course of the stimulus
expPara = struct('acqLen', 244, 'nStim', 20, ...
    'stimDur', 1.5, 'stimDly', 10.50, 'blankDur', 4.0);

% 2 blank periods (begin/end)
% (Stim + ISI) * N stim presentation
% randomly timed attention event
nStim = expPara.nStim;
stimDur = expPara.stimDur;
stimDly = expPara.stimDly;
blankDur = expPara.blankDur;

stimTime = 1:nStim;
stimTime = (stimTime - 1) * (stimDur + stimDly) + blankDur;

% load the data file for each session
allBeta = [];
base_dir = strcat('~/Data/fMRI', '/ORNT/', sub_name, '/', acq_type);
fprintf('Run preprocessing for %d sessions \n', n_session);

for idx = 1 : n_session
    
    ses_name = sprintf('func-%02d', idx);
    [cifti_data, motion_rg] = load_data(base_dir, ses_name);
    
    % High-pass filtering
    % load data
    spPeriod = 0.80;
    spRate = 1 / spPeriod;
    
    ts = cifti_data.cdata';
    ts = ts(:, roi_mask);
    sigTime = ((1 : size(ts, 1)) - 1) * spPeriod;
    
    % cutoff frequency
    cutoff = 1 / cutOffT;
    ts = highpass(ts, cutoff, spRate);
    
    % Motion regression
    % setup nuisance variables
    % decorrelation using PCA
    [~, score, latent] = pca(motion_rg);
    
    latent = latent / sum(latent);
    cum_lt = cumsum(latent);
    
    cutoff = sum(cum_lt < 1-1e-3);
    score = score(:, 1:cutoff);
    
    % setup motion nuisance regressors
    rgs = [score, ones(size(ts, 1), 1)];
    
    % solve with normal equation
    % save the residule as new time series
    theta = (rgs' * rgs) \ (rgs' * ts);
    ts = ts - rgs * theta;
    
    % Extract time course
    baseShift = 4.0;
    tRange = 0 : 0.8 : 4.0;
    signal = zeros(nStim, length(tRange), size(ts, 2));
    
    % get the time series
    for idy = 1:nStim
        target = stimTime(idy) + baseShift + tRange;
        value = interp1(sigTime, ts, target);
        signal(idy, :, :) = value;
    end
    
    % z-score for corresponding time point
    for idz = 1:length(tRange)
        value = signal(:, idz, :);
        arySize = size(value);
        
        % normalize
        value = squeeze(value);
        meanVec = mean(value, 1);
        stdVec = std(value, 0, 1);
        value = (value - meanVec) ./ stdVec;
        
        signal(:, idz, :) = reshape(value, arySize);
    end
    
    % beta (responses)
    beta = squeeze(mean(signal, 2));
    allBeta = [allBeta, beta'];
    
end

% Save results
if strcmp(saveDir, '')
    fl_path = fullfile('~/Data/fMRI/ORNT', sub_name, ...
    sprintf('%s_%s.mat', 'avg', acq_type));
else
    fl_dir = fullfile('~/Data/fMRI/ORNT', sub_name, 'roi', saveDir);

    if ~exist(fl_dir, 'dir')
       mkdir(fl_dir)
    end
    
    fl_path = fullfile(fl_dir, sprintf('%s_%s.mat', 'avg', acq_type));
end

results = struct('params', allBeta, 'v_label', v_label, 'e_label', e_label);
save(fl_path, 'results', 'sub_name', 'acq_type', 'roi_mask');

end