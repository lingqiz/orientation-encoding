%% Preprocessing with average response within a time window
% compute average and plot HRF
plotHRF = true;
run_avg_sub('ORNT_TW', 180, plotHRF);

%% Run processing for all subjects
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF'};
cutoff = 180;
for idx = 1:length(sub)    
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);
    run_avg_sub(sub_name, cutoff, false)
end

%% Helper Function
function run_avg_sub(sub_name, cutoff, plotHRF)
    
    n_runs = 10;
    n_sessions = 6;    
    
    if plotHRF
        figure();
        set(gcf,'Position',[0 0 1500 1500])
    end

    for idx = 1 : n_sessions
        acq_type = sprintf('Neural%02d', idx);
        fprintf('\nSession %s \n', acq_type);

        % average response        
        avg_resp(sub_name, acq_type, n_runs, cutoff);

        if plotHRF
            % compute HRF
            run_idx = randi(n_runs);
            [tRange, meanSig] = avg_hrf(sub_name, acq_type, run_idx);

            % plotting
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
    
end
