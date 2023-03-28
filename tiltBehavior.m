%% Analysis behavioral data from orientation estimation data
% 2023 LQZ
% This code was written to analysis data for the full experiment
% experiment codename: ORNT

% Run behavior.py in preprocess to convert JSON file to MAT format

%% Set library and data path
addpath('./analysis/');
addpath('./analysis/circstat/');

base = fullfile('~', 'Data', 'fMRI', 'ORNT');
subID = {'TW', 'MT', 'CMH', 'CR', 'SO'};

%% Plot data from individual subject
binSize = 12;
fiSmooth = 0.06;
allFi = cell(1, length(subID));

for idx = 1:length(subID)
    fullID = strcat('ORNT_', subID{idx});
    filePath = fullfile(base, fullID, strcat(fullID, '.mat'));
    data = load(filePath);
    
    [~, fi] = analysisSub(data.stim, data.resp, binSize, fiSmooth);
    allFi{idx} = fi;
end

%% Average FI pattern across individual subject
fiBase = zeros(size(fi{2}));
fi_1 = fiBase;
fi_2 = fiBase;

for idx = 1:length(subID)
    % FI for individual subject
    fi = allFi{idx};
    
    % accumulate FIs
    fiBase = fiBase + fi{2};
    fi_1 = fi_1 + fi{3};
    fi_2 = fi_2 + fi{4};
end

% compute average
support = fi{1};
fiBase = fiBase / length(subID);
fi_1 = fi_1 / length(subID);
fi_2 = fi_2 / length(subID);

%% Plot average the FI
figure();
set(gcf, 'units', 'points', ...
    'position', [0, 0, 650, 850]);

subplot(3, 2, 1);
plot(support, fiBase, 'k', 'LineWidth', 2);
xlabel('Orientation'); ylabel('Norm FI');
box off; grid off;

subplot(3, 2, 3);
plot(support, fi_1, 'k', 'LineWidth', 2);
xline(35.0, '--r', 'LineWidth', 2);
xlabel('Orientation'); ylabel('Norm FI');
box off; grid off;

subplot(3, 2, 5);
plot(support, fi_2, 'k', 'LineWidth', 2);
xline(145.0, '--r', 'LineWidth', 2);
xlabel('Orientation'); ylabel('Norm FI');
box off; grid off;

% difference from average FI
subplot(3, 2, 4);
plot(support, fi_1 - fiBase, 'k', 'LineWidth', 2);
xline(35.0, '--r', 'LineWidth', 2);
ylim([-0.1, 0.1]);
xlabel('Orientation'); ylabel('Delta FI');
box off; grid off;

subplot(3, 2, 6);
plot(support, fi_2 - fiBase, 'k', 'LineWidth', 2);
xline(145.0, '--r', 'LineWidth', 2);
ylim([-0.1, 0.1]);
xlabel('Orientation'); ylabel('Delta FI');
box off; grid off;

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

binSize = 12;
fiSmooth = 0.06;

[results, fi] = analysisSub(allStim, allResp, binSize, fiSmooth, false);

%% FI difference plot from combined subject
support = fi{1};
diff_1 = fi{3} - fi{2};
diff_2 = fi{4} - fi{2};

figure();
set(gcf, 'units', 'points', ...
    'position', [0, 0, 400, 750]);

subplot(2, 1, 1);
plot(support, diff_1, 'k', 'LineWidth', 2);
xline(35.0, '--r', 'LineWidth', 2);
ylim([-0.16, 0.16]);
ylabel('Delta FI');
box off; grid off;
figureFormat(2);

subplot(2, 1, 2);
plot(support, diff_2, 'k', 'LineWidth', 2);
xline(145.0, '--r', 'LineWidth', 2);
ylim([-0.16, 0.16]);
ylabel('Delta FI');
box off; grid off;
figureFormat(2);
