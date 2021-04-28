%% Setup path and plotting format
try
    tbUse('plotlab');
    plotlabOBJ = plotlab();
    plotlabOBJ.applyRecipe(...
        'figureWidthInches', 6, ...
        'figureHeightInches', 6);
catch EXP
    fprintf('plotlab not available, use default MATLAB style \n');
end

addpath('./CircStat/');
addpath('./ExpData/');

addpath('./cbrewer/');
colormap = cbrewer('seq', 'Greys', 9);

%% Load Data & Individual Subject
dataPath = 'ExpData/Adap_1/*.csv';
files = dir(dataPath);

for file = files'
    dataMtx  = readmatrix(fullfile(file.folder, file.name));
    
    % Analysis
    % moving average bin size
    binSize = 5;
    
    numBlock = 1;
    blockLength = 600;
    
    plotAll(dataMtx, numBlock, blockLength, binSize);
end

%% Combine data from blocks
dataPath = 'ExpData/Adap_1/*.csv';
files = dir(dataPath);

sLength = 600;
nBlock = 6;
nSubj  = 8;
bLength = sLength / nBlock;

dataBlocks = cell(1, nBlock);
for idx = 1:nBlock
    dataBlocks{idx} = [];
end

for file = files'
    dataMtx  = readmatrix(fullfile(file.folder, file.name));
    
    for idx = 1:nBlock
        dataBlock = dataBlocks{idx};
        dataBlock = [dataBlock, dataMtx(:, ((idx - 1) * bLength + 1) : idx * bLength)];
        dataBlocks{idx} = dataBlock;
    end
end

%% Data analysis
binSize = 16;
type = 'bias';

for idx = 1:nBlock
    dataBlock = dataBlocks{idx};
    result = analysisBlock(dataBlock, 'blockIndex', 1, 'blockLength',  bLength * nSubj, ...
        'binSize', binSize, 'mirror', true, 'smooth', false);
    
    switch type
        case 'bias'
            scatterPlot(result, 'showData', false, 'lineColor', colormap(idx + 1, :));
            ylim([-5, 5]);
            hold on;
            
        case 'var'
            stdvPlot(result, 'lineColor', colormap(idx + 1, :));
            hold on;
            
        case 'fisher'
            fisherPlot(result, 'smoothPara', 0.1, 'lineColor', colormap(idx + 1, :));
            hold on;
    end
end

%% Collect on the same plot
dataPath = 'ExpData/Adap_1/*.csv';
files = dir(dataPath);
type = 'fisher';
saveGif = true;

subIdx = 1;
fig = figure();
for file = files'
    
    dataMtx  = readmatrix(fullfile(file.folder, file.name));
    
    % Analysis
    % moving average bin size
    binSize = 5;
    
    numBlock = 1;
    blockLength = 600;
    
    result = analysisBlock(dataMtx, 'blockIndex', 1, 'blockLength', blockLength, ...
        'binSize', binSize, 'mirror', true, 'smooth', false);
    
    switch type
        case 'bias'
            scatterPlot(result, 'showData', false, 'lineColor', colormap(subIdx + 1, :));
            hold on;
            
        case 'var'
            stdvPlot(result, 'lineColor', colormap(subIdx + 1, :));
            hold on;
            
        case 'total'
            if subIdx == 1
                total = result.totalFI;
            else
                total = [total, result.totalFI];
            end
            
        case 'fisher'
            fisherPlot(result, 'smoothPara', 0.1, 'lineColor', colormap(subIdx + 1, :));
            hold on;
    end
    
    if saveGif
        % Capture the plot as an image
        frame = getframe(fig);
        img = frame2im(frame);
        [imgind, cm] = rgb2ind(img, 256);
        
        if subIdx == 1
            imwrite(imgind, cm, strcat('result', type, '.gif'), 'gif', 'Loopcount', inf);
        else
            imwrite(imgind, cm, strcat('result', type, '.gif'), 'gif', 'WriteMode', 'append');
        end
    end
    
    subIdx = subIdx + 1;
end

if strcmp(type, 'total')
    plot(1 : (subIdx - 1), total, '-ok');
    grid off; box off;
    xlabel('Session'); ylabel('Total FI');
    ylim([33, 38.5]); yticks(33:1:38);
end
