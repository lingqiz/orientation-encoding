%% Preprocessing with average response within a time window
sub_name = 'ORNT_TW';
n_runs = 10;
n_sessions = 6;
plot = false;

if plot
    figure();
    set(gcf,'Position',[0 0 1500 1500])
end

for idx = 1 : n_sessions    
    acq_type = sprintf('Neural%02d', idx);
    fprintf('\nSession %s \n', acq_type);
    
    % average response
    avg_resp(sub_name, acq_type, n_runs);
    
    % HRF
    run_idx = randi(n_runs);
    [tRange, meanSig] = avg_hrf(sub_name, acq_type, run_idx);
    
    % plotting
    if plot
        subplot(2, 3, idx);    
        plot(tRange, meanSig, '-ok', 'LineWidth', 1.5);
        
        xline(4.0, '--k'); xline(8.0, '--k');
        ylim([-0.75, 0.75])
        
        box off; grid off;
        xlabel('Time(s)');
        ylabel('Percent Signal Change');
        title(sprintf('Session %02d, Run %02d', idx, run_idx));
    end
end
