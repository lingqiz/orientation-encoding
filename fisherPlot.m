function fisherPlot(result, varargin)

p = inputParser;
p.addParameter('smoothPara', 0.1, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('lineColor', zeros(1, 3));
parse(p, varargin{:});

smoothPara = p.Results.smoothPara;
lineColor = p.Results.lineColor;

% smooth data beforehand (derivative is noisy
support = result.support;
average = smooth(result.average, smoothPara);
kappa   = smooth(result.kappa, smoothPara);

% fisher information calculation
fisher = abs((1 + gradient(average, support))) ./ sqrt(1 ./ kappa);
total_fisher = trapz(support, fisher);
norm_fisher  = fisher ./ total_fisher;

support = result.support / (2 * pi) * 180;
indice = (support > 2.5) & (support < 177.5);

plot(support(indice), norm_fisher(indice), 'k', 'LineWidth', 2, 'color', lineColor); hold on;

% axis labels and ticks
xlim([0, 180]);
xticks(0:45:180);
xlabel('Orientation (deg)');

ylim([0.05 0.35]);
ylabel('Normalized FI');

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

% format
grid off; box off;

end

