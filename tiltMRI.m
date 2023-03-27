%% Analysis behavioral data from orientation estimation data
% 2023 LQZ 
% This code was written to analysis data for the full experiment
% codename: ORNT

%% Setup path and plotting format
try
    tbUse('plotlab');
    plotlabOBJ = plotlab();
    plotlabOBJ.applyRecipe(...
        'figureWidthInches', 10, ...
        'figureHeightInches', 12);
catch EXP
    fprintf('plotlab not available, use default MATLAB style \n');
end

%% Set library path
addpath('./analysis/');
addpath('./analysis/circstat/');

%% Set data file path
% load data
base = fullfile('~', 'Data', 'fMRI', 'ORNT');
subID = {'TW', 'MT', 'CMH', 'CR', 'SO'};

% index the subject for analysis
index = [2];

% record data
allStim = [];
allResp = [];

for idx = index
    % setup file path
    fullID = strcat('ORNT_', subID{idx});
    filePath = fullfile(base, fullID, strcat(fullID, '.mat'));
    
    % load data file
    data = load(filePath);
    
    allStim = [allStim, data.stim];
    allResp = [allResp, data.resp];
end

%% Setup figure
allPlots = figure();

%% Analysis: baseline condition
binSize = 12;
numBlock = 1;
fiSmooth = 0.06;

condIdx = 1;
baseline = [allStim(condIdx, :); allResp(condIdx, :)];
result = analysisBlock(baseline, 'blockIndex', 1, 'blockLength', ...
    size(baseline, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 1);
scatterPlot(result);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 2);
fisherPlot(result, 'smoothPara', fiSmooth);

%% Analysis: surround condition 1
surround = 35.0;
condIdx = 2;
condData = [allStim(condIdx, :); allResp(condIdx, :)];
result = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
    size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 3);
scatterPlot(result);
xline(surround, '--r', 'LineWidth', 2);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 4);
fisherPlot(result, 'smoothPara', fiSmooth);
xline(surround, '--r', 'LineWidth', 2);

%% Analysis: surround condition 2
surround = 145.0;
condIdx = 3;
condData = [allStim(condIdx, :); allResp(condIdx, :)];
result = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
    size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 5);
scatterPlot(result);
xline(surround, '--r', 'LineWidth', 2);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 6);
[support, base_fisher] = fisherPlot(result, 'smoothPara', fiSmooth);
xline(surround, '--r', 'LineWidth', 2);
