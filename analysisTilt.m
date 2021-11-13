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

%% Set path
addpath('./analysis/');
addpath('./analysis/circstat/');

%% Load data
subID = {'LQZ', 'JM', 'BMC'};
index = [1, 2, 3];
dataMtx = [];

for idx = index
    path = fullfile('.', 'Behavior', subID{idx}, '*.csv');
    files = dir(path);
    for file = files'
        data = readmatrix(fullfile(file.folder, file.name));
        dataMtx = [dataMtx, data];
    end
end
%% Plot baseline data
plotStdv = false;
data = figure();
fisher = figure();

if plotStdv
    stdv = figure();
end

binSize = 12;
numBlock = 1;

baseline = dataMtx(2:end, isnan(dataMtx(1, :)));
result = analysisBlock(baseline, 'blockIndex', 1, 'blockLength', ...
    size(baseline, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
figure(data);
scatterPlot(result);

% fisherPlot applies addtional smoothing before calculating the FI
figure(fisher);
[support, base_fisher] = fisherPlot(result, 'smoothPara', 0.05);

if plotStdv
    figure(stdv);
    stdvPlot(result);
end

%% Plot other condition
cond = unique(dataMtx(1, :));
cond = cond(~isnan(cond));

for surround = cond
    condData = dataMtx(2:end, dataMtx(1, :) == surround);
    result = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
        size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);
    
    data = figure();
    fisher = figure();
    
    if plotStdv
        stdv = figure();
    end
    
    figure(data); hold on;
    scatterPlot(result);
    xline(surround, '--r', 'LineWidth', 2);
    
    % fisherPlot applies addtional smoothing before calculating the FI
    figure(fisher); hold on;
    fisherPlot(result, 'smoothPara', 0.05);
    xline(surround, '--r', 'LineWidth', 2);
    
    if plotStdv
        figure(stdv); hold on;
        stdvPlot(result);
        xline(surround, '--r', 'LineWidth', 2);
    end
end

%% plot the difference in norm fisher
cond = unique(dataMtx(1, :));
cond = cond(~isnan(cond));

for surround = cond
    condData = dataMtx(2:end, dataMtx(1, :) == surround);
    result = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
        size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);
    
    figure(); hold on;
    [~, cond_fisher] = fisherPlot(result, 'smoothPara', 0.05, 'showPlot', false);
    
    plot(support, cond_fisher - base_fisher, 'k', 'LineWidth', 2);
    
    % axis labels and ticks
    xlim([0, 180]); xticks(0:45:180);
    xlabel('Orientation (deg)');
    
    ylim([-0.15 0.15]); yline(0, '--');
    ylabel('Diff in Norm FI');
    
    % add reference lines
    xline(45, '--'); xline(90, '--'); xline(135, '--');
    xline(surround, '--r', 'LineWidth', 2);
    
    % format
    grid off; box off;
end
