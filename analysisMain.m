%% Setup path and plotting format
try 
    tbUse('plotlab');
    plotlabOBJ = plotlab();
    plotlabOBJ.applyRecipe(...
        'figureWidthInches', 20, ...
        'figureHeightInches', 8);           
catch EXP
    fprintf('plotlab not available, use default MATLAB style \n');
end

addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
fileName = {'10_11_2020_18_04_LQ_0.csv', '11_11_2020_09_08_LQ_0.csv', ...
    '13_11_2020_18_30_LQ_1.csv', '14_11_2020_18_51_taka_0.csv'...,
    '15_11_2020_14_53_LQ_1.csv', '18_11_2020_18_20_QC_0.csv', ...
    '19_11_2020_19_18_taka_0.csv', '23_11_2020_17_44_QC_0.csv'};

subId = 8;
dataMtx  = readmatrix(fileName{subId});

% Analysis
% moving average bin size
binSize = 15;

numBlock = 3;
blockLength = 200;

plotAll(dataMtx, numBlock, blockLength, binSize);
