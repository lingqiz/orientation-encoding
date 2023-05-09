function stdvPlot(result, varargin)

p = inputParser;
p.addParameter('lineColor', zeros(1, 3));
p.addParameter('sdRange', [0, 20]);
parse(p, varargin{:});

lineColor = p.Results.lineColor;
sdRange = p.Results.sdRange;

support = result.support / (2 * pi) * 180;
stdv = result.stdv / (2 * pi) * 180;

plot(support, stdv, 'k', 'LineWidth', 2, 'color', lineColor); hold on;
title(strcat('Total FI:', num2str(result.totalFI)));

% axis and axis ticks
xlim([0, 180]);
ylim(sdRange);
xticks(0:45:180);
xlabel('Orientation (deg)');
ylabel('S.D. (deg)');

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

% format
grid off; box off;

end

