%% Setup Path
addpath('./CircStat/');
addpath('./ExpData/');

%% Load Data
fileName = '10_11_2020_18_04_LQ_0.csv';
% fileName = '11_11_2020_09_08_LQ_0.csv';
dataMtx  = readmatrix(fileName);

%% Analysis
% figure();
subplot(1, 3, 1);
scatterPlot(dataMtx, 1);

subplot(1, 3, 2);
scatterPlot(dataMtx, 2);

subplot(1, 3, 3);
scatterPlot(dataMtx, 3);

%% Helper Function
function scatterPlot(dataMtx, blockIndex)

blockLength = 200;

idxL = (blockIndex - 1) * blockLength + 1;
idxH = blockIndex * blockLength;

target = dataMtx(1, idxL:idxH)';
response = dataMtx(2, idxL:idxH)';

mirror = false;
[target, bias, average, ~, support] = computeStat(target, response, 15, mirror);

target  = target / (2 * pi) * 180;
bias    = bias / (2 * pi) * 180;
support = support / (2 * pi) * 180;
average = average / (2 * pi) * 180;

scatter(target, bias, 'k'); hold on;
plot(support, average, 'k', 'LineWidth', 2); hold on;

xlim([0, 180]);
ylim([-25, 25]);

xline(45);
xline(90);
xline(135);
yline(0);

end