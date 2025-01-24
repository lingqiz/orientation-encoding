% Run processing for different ROIs
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

    run_avg_sub(sub_name, 'areaIndex', [11, 12], ...
        'eccLo', 1.0, 'eccHi', 15.0, 'saveDir', 'V3A_B_Large');
end

%% Using pRF to define ROIs
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 0, 'eccHi', 1.5, ...
        'saveDir', 'pRF_0', 'prfROI', 2);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 1.5, 'eccHi', 5, ...
        'saveDir', 'pRF_1', 'prfROI', 2);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 5, 'eccHi', 9, 'saveDir', 'pRF_2');

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 9, 'eccHi', 15, ...
        'saveDir', 'pRF_3', 'prfROI', 1);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'eccLo', 15, 'eccHi', 30, ...
        'saveDir', 'pRF_4', 'prfROI', 1);
end

%% Define ROI based on polar angle (V1 - V3)
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

% for +35 surround
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'polarLo', 5, 'polarHi', 65, ...
        'saveDir', 'PolarPosCon', 'prfROI', 3);
end

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'polarLo', 95, 'polarHi', 155, ...
        'saveDir', 'PolarPosInc', 'prfROI', 3);
end

% for -35 surround
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'polarLo', 115, 'polarHi', 175, ...
        'saveDir', 'PolarNegCon', 'prfROI', 3);
end

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'polarLo', 25, 'polarHi', 85, ...
        'saveDir', 'PolarNegInc', 'prfROI', 3);
end

% tangent angle
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'saveDir', 'PolarPosSide', 'prfROI', 4);
end

for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});
    fprintf(sub_name);

    run_avg_sub(sub_name, 'areaIndex', [1, 2, 3], ...
        'saveDir', 'PolarNegSide', 'prfROI', 5);
end

%% Visual Eccentricity of pRF center (Deprecated)
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
