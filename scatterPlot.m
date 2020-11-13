function scatterPlot(result)

% from rad to deg
target  = result.target / (2 * pi) * 180;
bias = result.bias / (2 * pi) * 180;
support = result.support / (2 * pi) * 180;
average = result.average / (2 * pi) * 180;

markerColor = ones(1, 3) * 0.5;
scatter(target, bias, 12, 'MarkerFaceColor', markerColor, 'MarkerEdgeColor', markerColor); hold on;
plot(support, average, 'k', 'LineWidth', 2); hold on;

xlim([0, 180]);
ylim([-25, 25]);

xticks(0:45:180);
yticks(-25:10:25);

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');
yline(0, '--');

end