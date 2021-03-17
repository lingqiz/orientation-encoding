function plotAll(dataMtx, numBlock, blockLength, binSize)    
    stim = figure();
    data = figure();
    stdv = figure();
    fisher = figure();

    for idx = 1 : numBlock
        figure(stim);
        subplot(1, numBlock, idx);
        histogram(dataMtx(1, ((idx - 1) * blockLength + 1) : idx * blockLength), 20);
        
        % axis and axis ticks
        box off; grid off;
        xlim([0, 180]); xticks(0:45:180);
        xlabel('Orientation (deg)');

        % analysis data of the particular block with computeStat function
        result = analysisBlock(dataMtx, 'blockIndex', idx, 'blockLength', blockLength, ...
            'binSize', binSize, 'mirror', true, 'smooth', false);

        % plot data and stats
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