%% Setup path and plotting format
try
    tbUse('plotlab');
    plotlabOBJ = plotlab();
    plotlabOBJ.applyRecipe(...
        'figureWidthInches', 12, ...
        'figureHeightInches', 8);
catch EXP
    fprintf('plotlab not available, use default MATLAB style \n');
end

%% Load data
mtx_1 = readmatrix(fullfile('TiltData', '03_10_2021_20_11_tilt_1.csv'));
mtx_2 = readmatrix(fullfile('TiltData', '04_10_2021_08_26_tilt_2.csv'));

dataMtx = [mtx_1, mtx_2];

%% Load data
addpath('./analysis/');
addpath('./analysis/circstat/');

dataMtx = [];

files = dir('./TiltData/*_tilt_final.csv');
for file = files'
    data = readmatrix(fullfile(file.folder, file.name));
    dataMtx = [dataMtx, data];
end

%% Plot baseline data
data = figure();
stdv = figure();
fisher = figure();

binSize = 15;
numBlock = 1;
mirror = false; 

baseline = dataMtx(2:end, isnan(dataMtx(1, :)));
result = analysisBlock(baseline, 'blockIndex', 1, 'blockLength', ...
    size(baseline, 2), 'binSize', binSize, 'mirror', false, 'smooth', true);

% plot data and stats
figure(data);
scatterPlot(result);

figure(stdv);
stdvPlot(result);

% fisherPlot applies addtional smoothing before calculating the FI
figure(fisher);
fisherPlot(result, 'smoothPara', 0.075);

%% Plot other condition
cond = unique(dataMtx(1, :));
cond = cond(~isnan(cond));

for surround = cond
    condData = dataMtx(2:end, dataMtx(1, :) == surround);
    result = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
        size(condData, 2), 'binSize', binSize, 'mirror', mirror, 'smooth', true);
    
    data = figure();
    stdv = figure();
    fisher = figure();
    
    figure(data); hold on;
    scatterPlot(result);
    xline(surround, '--r', 'LineWidth', 2);
    
    figure(stdv); hold on;
    stdvPlot(result);
    xline(surround, '--r', 'LineWidth', 2);
    
    % fisherPlot applies addtional smoothing before calculating the FI
    figure(fisher); hold on;
    fisherPlot(result, 'smoothPara', 0.075);
    xline(surround, '--r', 'LineWidth', 2);
end
