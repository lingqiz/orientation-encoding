%% Run processing for different ROIs
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

% Cond 1: Control
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'nonVisual', true, 'saveDir', 'NonVisual');
end

%% Cond 2 - 3: [V1; V2 + V3] (Early vs. Late)
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', 1, ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'V1');

    run_avg_sub(sub_name, 'areaIndex', [2, 3], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'V2_V3');
end

%% Higher visual area
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    % hV4 + VO1
    run_avg_sub(sub_name, 'areaIndex', [4, 5, 6], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'HV4_VO1_2');

    % V3a + V3b
    run_avg_sub(sub_name, 'areaIndex', [11, 12], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'V3A_B');

    % LO1 + LO2
    run_avg_sub(sub_name, 'areaIndex', [7, 8], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'LO1_2');
end

%% Visual Eccentricity
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    % Select voxel from different eccentricity
    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.0, 'eccHi', 5.0, 'saveDir', 'Stim_Inner');

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 5.0, 'eccHi', 12.5, 'saveDir', 'Stim_Outer');

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 12.5, 'eccHi', 30.0, 'saveDir', 'Stim_Surround');

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 30.0, 'eccHi', 90.0, 'saveDir', 'Stim_Null');
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