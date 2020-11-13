%% Setup Path
addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
fileName = '10_11_2020_18_04_LQ_0.csv';
fileName = '11_11_2020_09_08_LQ_0.csv';
dataMtx  = readmatrix(fileName);

%% Analysis
% moving average bin size
binSize = 18;

figure();
subplot(1, 3, 1);
result = analysisBlock(dataMtx, 'blockIndex', 1, 'binSize', binSize);
scatterPlot(result);

subplot(1, 3, 2);
result = analysisBlock(dataMtx, 'blockIndex', 2, 'binSize', binSize);
scatterPlot(result);

subplot(1, 3, 3);
result = analysisBlock(dataMtx, 'blockIndex', 3, 'binSize', binSize);
scatterPlot(result);
