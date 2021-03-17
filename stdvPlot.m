function stdvPlot(result, varargin)

p = inputParser;
p.addParameter('lineColor', zeros(1, 3));
parse(p, varargin{:});

lineColor = p.Results.lineColor;

support = result.support / (2 * pi) * 180;
stdv = result.stdv / (2 * pi) * 180;

plot(support, stdv, 'k', 'LineWidth', 2, 'color', lineColor); hold on;
title(strcat('Total FI:', num2str(result.totalFI)));

% axis and axis ticks
xlim([0, 180]);
ylim([0, 15]);
xticks(0:45:180);
xlabel('Orientation (deg)');
ylabel('1/Kappa');

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

% format
grid off; box off;

end

