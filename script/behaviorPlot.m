%% Set library and data path
addpath('../analysis/');
addpath('../analysis/circstat/');

base = fullfile('~', 'Data', 'fMRI', 'ORNT');
subID = {'TW', 'MT', 'CMH', 'CR', 'SO', 'BH', 'DW', 'QF', 'JM', 'MA'};

%% Combined Subject
index = 1:length(subID);

% record data
allStim = [];
allResp = [];

for idx = index
    % setup file path
    fullID = strcat('ORNT_', subID{idx});
    filePath = fullfile(base, fullID, strcat(fullID, '.mat'));

    % load data file
    data = load(filePath);

    allStim = [allStim, data.stim];
    allResp = [allResp, data.resp];
end

%% Extract Statistics
fileName = {'Base', 'Surr1', 'Surr2'};

for condIdx = 1:3   
    condData = [allStim(condIdx, :); allResp(condIdx, :)];

    nRun = 500;
    [~, average, stdv, fisher] = statAll(condData);
    [support, allAverage, allStdv, allFisher] = statBootstrap(condData, nRun);

    name = sprintf('./%s.mat', fileName{condIdx});
    save(name, 'support', 'average', 'stdv', ...
        'fisher', 'allAverage', 'allStdv', 'allFisher');
end
