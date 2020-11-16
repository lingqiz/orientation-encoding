%% Setup Path
addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
fileName = {'10_11_2020_18_04_LQ_0.csv', '11_11_2020_09_08_LQ_0.csv', ...
    '13_11_2020_18_30_LQ_1.csv', '14_11_2020_18_51_taka_0.csv'...,
    '15_11_2020_14_53_LQ_1.csv'};

subId = 1;
dataMtx  = readmatrix(fileName{subId});

% Analysis
% moving average bin size
binSize = 18;

numBlock = 3;
blockLength = 200;

plotAll(dataMtx, numBlock, blockLength, binSize);

%% Helper Function
function plotAll(dataMtx, numBlock, blockLength, binSize)
    figSize = [100 100 1000 400];
    stim = figure('Position', figSize);
    data = figure('Position', figSize);
    stdv = figure('Position', figSize);
    fisher = figure('Position', figSize);

    for idx = 1 : numBlock
        figure(stim);
        subplot(1, numBlock, idx);
        histogram(dataMtx(1, ((idx - 1) * blockLength + 1) : idx * blockLength), 20);

        % analysis data of the particular block with computeStat function
        result = analysisBlock(dataMtx, 'blockIndex', idx, 'blockLength', blockLength, ...
            'binSize', binSize, 'mirror', true, 'smooth', false);

        figure(data);
        subplot(1, numBlock, idx);
        scatterPlot(result);

        figure(stdv);
        subplot(1, numBlock, idx);
        stdvPlot(result);

        % fisherPlot applies addtional smoothing before calculating the FI
        figure(fisher);
        subplot(1, numBlock, idx);
        fisherPlot(result, 'smoothPara', 0.075);
    end
end
