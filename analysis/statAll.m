function [support, average, stdv, fisher] = statAll(dataBlock)

result = analysisBlock(dataBlock, 'blockIndex', 1, 'blockLength', ...
    size(dataBlock, 2), 'binSize', 18, 'period', false, 'smooth', true);

support = result.support / (2 * pi) * 180;
support = support';

average = result.average / (2 * pi) * 180;
stdv = result.stdv / (2 * pi) * 180;

[~, fisher] = fisherPlot(result, 'smoothPara', 0.05, ...
                         'cutOff', false, 'showPlot', false);

end

