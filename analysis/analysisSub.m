function [allResult, allFisher] = analysisSub(allStim, allResp, binSize, fiSmooth, scatter, sdRange)

%% Setup
figure();
set(gcf, 'units', 'points', ...
    'position', [0, 0, 650, 850]);

if ~exist('scatter', 'var')
    scatter = 'true';
end

if ~exist('scatter', 'var')
    sdRange = [0, 20];
end

%% Analysis: baseline condition

condIdx = 1;
baseline = [allStim(condIdx, :); allResp(condIdx, :)];
result_1 = analysisBlock(baseline, 'blockIndex', 1, 'blockLength', ...
    size(baseline, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 3, 1);
scatterPlot(result_1, 'showData', scatter);
figureFormat(1);

% plot standard deviation
subplot(3, 3, 2);
stdvPlot(result_1, 'sdRange', sdRange);
figureFormat(1);
title('');

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 3, 3);
[support, fisher_1] = fisherPlot(result_1, 'smoothPara', fiSmooth);
figureFormat(1);

%% Analysis: surround condition 1
surround = 35.0;
condIdx = 2;
condData = [allStim(condIdx, :); allResp(condIdx, :)];
result_2 = analysisBlock(condData, 'blockIndex', 1, 'blockLength', ...
    size(condData, 2), 'binSize', binSize, 'period', false, 'smooth', true);

% plot data and stats
subplot(3, 3, 4);
scatterPlot(result_2, 'showData', scatter);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

% plot standard deviation
subplot(3, 3, 5);
stdvPlot(result_2, 'sdRange', sdRange);
figureFormat(1);
title('');

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 3, 6);
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
subplot(3, 3, 7);
scatterPlot(result_3, 'showData', scatter);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

% plot standard deviation
subplot(3, 3, 8);
stdvPlot(result_3, 'sdRange', sdRange);
figureFormat(1);
title('');

% fisherPlot applies addtional smoothing before calculating the FI
subplot(3, 3, 9);
[~, fisher_3] = fisherPlot(result_3, 'smoothPara', fiSmooth);
xline(surround, '--r', 'LineWidth', 2);
figureFormat(1);

%% Return value
allResult = {result_1, result_2, result_3};
allFisher = {support, fisher_1, fisher_2, fisher_3};

end 