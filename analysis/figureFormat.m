function figureFormat(option)

if option == 1
    set(gca, 'linewidth', 1);
    set(gca, 'TickDir', 'out');
    set(gca, 'TickLength', [0.02, 0.025]);

    ax = gca;
    ax.XAxis.FontSize = 14;
    ax.YAxis.FontSize = 14;
end

if option == 2
    set(gca, 'linewidth', 1);
    set(gca, 'TickDir', 'out');
    set(gca, 'TickLength', [0.02, 0.025]);

    ax = gca;
    ax.XAxis.FontSize = 14;
    ax.YAxis.FontSize = 14;

    xlim([0, 180]);
    xticks(0:45:180);
    xlabel('Orientation (deg)');

    yline(0.0, '--k', 'LineWidth', 1);
end

end