%% Setup Path
addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
fileName = '10_11_2020_18_04_LQ_0.csv';
fileName = '11_11_2020_09_08_LQ_0.csv';
fileName = '13_11_2020_18_30_LQ_1.csv';
fileName = '14_11_2020_18_51_taka_0.csv';
dataMtx  = readmatrix(fileName);

% Analysis
% moving average bin size
binSize = 20;

numBlock = 3;
blockLength = 200;

plotAll(dataMtx, numBlock, blockLength, binSize);

%% Helper Function
function plotAll(dataMtx, numBlock, blockLength, binSize)
    stim = figure();
    data = figure();
    % fisher = figure();
    for idx = 1 : numBlock
        figure(stim);
        subplot(1, numBlock, idx);
        histogram(dataMtx(1, ((idx - 1) * blockLength + 1) : idx * blockLength), 20);
        
        result = analysisBlock(dataMtx, 'blockIndex', idx, 'blockLength', blockLength, 'binSize', binSize);
        figure(data);
        subplot(1, numBlock, idx);
        scatterPlot(result);
        
        figure(fisher);
        subplot(1, numBlock, idx);
        fisherPlot(result);
    end
end