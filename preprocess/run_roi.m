%% Run processing for different ROIs
% Cond 1: Control

sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 12, 'eccHi', 25, 'saveDir', 'control');
end

%% Cond 2 - 3: [V1; V2 + V3] (Early vs. Late)
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'control');
end

%% hV4 + VO1

%% V3a + V3b

%% LO1 + LO2

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