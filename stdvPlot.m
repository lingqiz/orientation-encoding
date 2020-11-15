function stdvPlot(result)

support = result.support / (2 * pi) * 180;
stdv = result.stdv / (2 * pi) * 180;

plot(support, stdv, 'k', 'LineWidth', 2); hold on;
title(strcat('Total FI:', num2str(result.totalFI)));

% axis and axis ticks
xlim([0, 180]);
ylim([5, 15]);
xticks(0:45:180);

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

end

