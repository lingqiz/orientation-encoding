function [support, norm_fisher] = fisherPlot(result, varargin)

p = inputParser;
p.addParameter('smoothPara', 0.1, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('lineColor', zeros(1, 3));
p.addParameter('cutOff', true);
p.addParameter('showPlot', true);
parse(p, varargin{:});

smoothPara = p.Results.smoothPara;
lineColor = p.Results.lineColor;
cutOff = p.Results.cutOff;
showPlot = p.Results.showPlot;

% smooth data beforehand (derivative is noisy)
support = result.support;
average = smooth(result.average, smoothPara);
kappa   = smooth(result.kappa, smoothPara);

% fisher information calculation
fisher = abs((1 + gradient(average, support))) ./ sqrt(1 ./ kappa);
total_fisher = trapz(support, fisher);
norm_fisher  = fisher ./ total_fisher;

if cutOff
    support = result.support / (2 * pi) * 180;
    indice = (support > 2.5) & (support < 177.5);

    support = support(indice);
    norm_fisher = norm_fisher(indice);
end

if showPlot
    plot(support, norm_fisher, 'k', 'LineWidth', 2, 'color', lineColor); hold on;
    
    % axis labels and ticks
    xlim([0, 180]);
    xticks(0:45:180);
    xlabel('Orientation (deg)');
    
    ylim([0.0 0.40]);
    yticks(0:0.1:0.4);
    ylabel('Normalized FI');
    
    % add reference lines
    xline(45, '--');
    xline(90, '--');
    xline(135, '--');
    
    % format
    grid off; box off;
end

end

