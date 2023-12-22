%% Run processing for different ROIs
% Base: V1 - V3, 1.5 deg - 12.5 (Full Stimulus Range)
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.5, 'eccHi', 12.5, 'saveDir', 'Stim_Visual');

    run_avg_sub(sub_name, 'areaIndex', [1], ...
        'eccLo', 1.5, 'eccHi', 12.5, 'saveDir', 'Stim_V1');

    run_avg_sub(sub_name, 'areaIndex', [2, 3], ...
        'eccLo', 1.5, 'eccHi', 12.5, 'saveDir', 'Stim_V2_V3');

    run_avg_sub(sub_name, 'areaIndex', [4, 5, 6], ...
        'eccLo', 1.5, 'eccHi', 12.5, 'saveDir', 'Stim_HV4_VO1_2');
end

%% Base: V1 - V3
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.0, 'eccHi', 7.0, 'saveDir', 'V1_V2_V3');
end

%% Control: Motor or Auditory Cortex
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

% Cond 1: Control
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'nonVisual', 2, 'saveDir', 'Motor');
    run_avg_sub(sub_name, 'nonVisual', 3, 'saveDir', 'Auditory');
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

bins = round(cumsum(2 .^ (0:1.02:6)));
binEdge = [0, bins];

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(strcat(sub_name, '\n'));

    % Select voxel from different eccentricity
    for idy = 1:(length(binEdge) - 1)
        fprintf('\nEcc %d - %d', binEdge(idy), binEdge(idy + 1))

        run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
            'eccLo', binEdge(idy), 'eccHi', binEdge(idy + 1), ...
            'saveDir', sprintf('EccBin_%d', idy));
    end
end

%% Use Larger Ecc ROIs
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', 1, ...
        'eccLo', 1.0, 'eccHi', 15.0, 'saveDir', 'V1_Large');

    run_avg_sub(sub_name, 'areaIndex', [2, 3], ...
        'eccLo', 1.0, 'eccHi', 15.0, 'saveDir', 'V2_V3_Large');

    run_avg_sub(sub_name, 'areaIndex', [4, 5, 6], ...
        'eccLo', 1.0, 'eccHi', 15.0, 'saveDir', 'HV4_VO1_2_Large');
end

%% Using pRF to define ROIs
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.5, 'eccHi', 5, ...
        'saveDir', 'pRF_Center', 'prfROI', 2);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 9, 'eccHi', 12.5, ...
        'saveDir', 'pRF_Surround', 'prfROI', 1);
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
