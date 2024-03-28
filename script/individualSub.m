%% Set library and data path
addpath('../analysis/');
addpath('../analysis/circstat/');

base = fullfile('~', 'Data', 'fMRI', 'ORNT');
subID = {'TW', 'MT', 'CMH', 'CR', 'SO', 'BH', 'DW', 'QF', 'JM', 'MA'};

%% Loop through each subject
index = 1:length(subID);

for idx = index
    % setup file path
    fullID = strcat('ORNT_', subID{idx});
    filePath = fullfile(base, fullID, strcat(fullID, '.mat'));

    % load data file
    data = load(filePath);

    % Bootstrap statistics
    fileName = {'Base', 'Surr1', 'Surr2'};

    for condIdx = 1:3
        condData = [data.stim(condIdx, :); data.resp(condIdx, :)];

        nRun = 500;
        [~, average, stdv, fisher] = statAll(condData);
        [support, allAverage, allStdv, allFisher] = statBootstrap(condData, nRun);

        name = sprintf('./%s_%s.mat', subID{idx}, fileName{condIdx});
        save(name, 'support', 'average', 'stdv', ...
            'fisher', 'allAverage', 'allStdv', 'allFisher');
    end
end

