function fisherPlot(result)

support = result.support / (2 * pi) * 180;
plot(support, result.patternFI, 'k', 'LineWidth', 2); hold on;

xlim([0, 180]);
xticks(0:45:180);

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

end

