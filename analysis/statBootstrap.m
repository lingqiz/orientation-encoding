function [support, allAverage, allStdv, allFisher] = statBootstrap(dataBlock, nRun)

% compute stats for a single block
[support, ~, ~, ~] = statAll(dataBlock);

allAverage = zeros(length(support), nRun);
allStdv = zeros(length(support), nRun);
allFisher = zeros(length(support), nRun);

% bootstrapping runs
nData = size(dataBlock, 2);
for idx = 1:nRun
    dataIndex = randsample(nData, nData, true);
    sampleData = dataBlock(:, dataIndex);

    [support, average, stdv, fisher] = statAll(sampleData);
    
    allAverage(:, idx) = average;
    allStdv(:, idx) = stdv;
    allFisher(:, idx) = fisher;
end

end