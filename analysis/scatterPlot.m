function scatterPlot(result, varargin)

p = inputParser;
p.addParameter('showData', true);
p.addParameter('lineColor', zeros(1, 3));
parse(p, varargin{:});

showData  = p.Results.showData;
lineColor = p.Results.lineColor;

% from rad to deg
target  = result.target / (2 * pi) * 180;
bias = result.bias / (2 * pi) * 180;
support = result.support / (2 * pi) * 180;
average = result.average / (2 * pi) * 180;

markerColor = ones(1, 3) * 0.5;
if showData
    scatter(target, bias, 12, 'MarkerFaceColor', markerColor, 'MarkerEdgeColor', markerColor); hold on;
end

plot(support, average, 'k', 'LineWidth', 2, 'color', lineColor); hold on;

% axis and axis ticks
xlim([0, 180]);
ylim([-15, 15]);

xticks(0:45:180);
xlabel('Orientation (deg)');

yticks(-15:5:15);
ylabel('Bias (deg)');

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');
yline(0, '--');

% format
grid off; box off;

end