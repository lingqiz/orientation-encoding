function result = analysisBlock(dataMtx, varargin)

p = inputParser;
p.addParameter('blockIndex', 1, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('blockLength', 200, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('binSize', 5, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('period', false, @islogical);
p.addParameter('smooth', false, @islogical);
parse(p, varargin{:});

blockIndex   = p.Results.blockIndex;
blockLength = p.Results.blockLength;

idxL = (blockIndex - 1) * blockLength + 1;
idxH = blockIndex * blockLength;

target = dataMtx(1, idxL:idxH)';
response = dataMtx(2, idxL:idxH)';

result = computeStat(target, response, 'binSize', p.Results.binSize, ...
    'period', p.Results.period, 'smooth', p.Results.smooth);

end

