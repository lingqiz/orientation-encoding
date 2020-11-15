function fisherPlot(result, varargin)

p = inputParser;
p.addParameter('smoothPara', 0.1, @(x)(isnumeric(x) && numel(x) == 1));
parse(p, varargin{:});

smoothPara = p.Results.smoothPara;

% smooth data beforehand (derivative is noisy
support = result.support;
average = smooth(result.average, smoothPara);
kappa   = smooth(result.kappa, smoothPara);

% fisher information calculation
fisher = abs((1 + gradient(average, support))) ./ sqrt(1 ./ kappa);
total_fisher = trapz(support, fisher);
norm_fisher  = fisher ./ total_fisher;

support = result.support / (2 * pi) * 180;
indice = (support > 2) & (support < 178);

title('Norm FI');
plot(support(indice), norm_fisher(indice), 'k', 'LineWidth', 2); hold on;

xlim([0, 180]);
xticks(0:45:180);
ylim([0. 0.3]);

% add reference lines
xline(45, '--');
xline(90, '--');
xline(135, '--');

end

