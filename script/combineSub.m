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

binSize = 12;
fiSmooth = 0.05;

[results, fi] = analysisSub(allStim, allResp, binSize, fiSmooth, false, [5, 15]);
set(gcf, 'units', 'points', ...
    'position', [0, 0, 975, 850]);

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
