function [allResult, allFisher] = analysisSub(allStim, allResp, binSize, fiSmooth, scatter)

%% Setup
figure();
set(gcf, 'units', 'points', ...
    'position', [0, 0, 650, 850]);

if ~exist('scatter', 'var')
    scatter = 'true';
end

%% Analysis: baseline condition

condIdx = 1;
baseline = [allStim(condIdx, :); allResp(condIdx, :)];
result_1 = analysisBlock(baseline, 'blockIndex', 1, 'blockLength', ...
    size(baseline, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 1);
scatterPlot(result_1, 'showData', scatter);
figureFormat(1);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 2);
[support, fisher_1] = fisherPlot(result_1, 'smoothPara', fiSmooth);
figureFormat(1);

%% Analysis: surround condition 1
surround = 35.0;
condIdx = 2;
condData = [allStim(condIdx, :); allResp(condIdx, :)];
result_2 = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
    size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 3);
scatterPlot(result_2, 'showData', scatter);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 4);
[~, fisher_2] = fisherPlot(result_2, 'smoothPara', fiSmooth);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

%% Analysis: surround condition 2
surround = 145.0;
condIdx = 3;
condData = [allStim(condIdx, :); allResp(condIdx, :)];
result_3 = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
    size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 2, 5);
scatterPlot(result_3, 'showData', scatter);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 2, 6);
[~, fisher_3] = fisherPlot(result_3, 'smoothPara', fiSmooth);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

%% Return value
allResult = {result_1, result_2, result_3};
allFisher = {support, fisher_1, fisher_2, fisher_3};

end 