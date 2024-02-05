%% Count Number of Voxels across ROIs
addpath('cifti-matlab');

%% V1
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

count = zeros(1, length(sub));
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});

    % V1
    [roi_mask, v_label, e_label] = define_roi(sub_name, 'areaIndex', 1, ...
                                            'eccLo', 1, 'eccHi', 7, ...
                                            'nonVisual', 0, 'prfROI', 0);
    count(idx) = sum(roi_mask);
end

fprintf('%d +/- %d \n', round(mean(count)), round(std(count)));

%% V2/3
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

count = zeros(1, length(sub));
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});

    % V1
    [roi_mask, v_label, e_label] = define_roi(sub_name, 'areaIndex', [2, 3], ...
                                            'eccLo', 1, 'eccHi', 7, ...
                                            'nonVisual', 0, 'prfROI', 0);
    count(idx) = sum(roi_mask);
end

fprintf('%d +/- %d \n', round(mean(count)), round(std(count)));

%% V4/VO1/2
sub = {'TW', 'MT', 'CMH', 'SO', 'CR', 'BH', 'DW', 'QF', 'JM', 'MA'};

count = zeros(1, length(sub));
for idx = 1:length(sub)
    sub_name = strcat('ORNT_', sub{idx});

    % V1
    [roi_mask, v_label, e_label] = define_roi(sub_name, 'areaIndex', [4, 5, 6], ...
                                            'eccLo', 1, 'eccHi', 7, ...
                                            'nonVisual', 0, 'prfROI', 0);
    count(idx) = sum(roi_mask);
end

fprintf('%d +/- %d \n', round(mean(count)), round(std(count)));

