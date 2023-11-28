%% Run processing for all subjects
% Cond 1: Control (7.5 - 12.5 deg eccentricity)

sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 7.5, 'eccHi', 12.5, 'saveDir', 'control');
end

%% Helper Function
function run_avg_sub(sub_name, varargin)

n_runs = 10;
n_sessions = 6;

for idx = 1 : n_sessions
    acq_type = sprintf('Neural%02d', idx);
    fprintf('\nSession %s \n', acq_type);
    
    % average response
    avg_resp(sub_name, acq_type, n_runs, varargin{:});
end

end