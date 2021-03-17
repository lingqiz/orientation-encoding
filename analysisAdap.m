%% Setup path and plotting format
try 
    tbUse('plotlab');
    plotlabOBJ = plotlab();
    plotlabOBJ.applyRecipe(...
        'figureWidthInches', 14, ...
        'figureHeightInches', 6);           
catch EXP
    fprintf('plotlab not available, use default MATLAB style \n');
end

addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
dataPath = 'ExpData/Adap_1/*.csv';
files = dir(dataPath);

for file = files'
    dataMtx  = readmatrix(fullfile(file.folder, file.name));
        
    % Analysis
    % moving average bin size
    binSize = 15;

    numBlock = 3;
    blockLength = 200;

    plotAll(dataMtx, numBlock, blockLength, binSize);
end