function [roi_mask, v_label, e_label] = define_roi(sub_name, varargin)

p = inputParser;

% Stimulus: 0 - 1.5 deg; 1.5 - 7 deg; > 7 deg

% Area - Index Correspondence
% {1:  'V1',   2: 'V2',  3: 'V3',  4: 'hV4',  5: 'VO1', 6:  'VO2',
% 7: 'LO1', 8: 'LO2', 9: 'TO1', 10: 'TO2', 11: 'V3b', 12: 'V3a'}

% Default ROI: V1 - V3 area, foeval (1.0) - 7.0 degree eccentricity
p.addParameter('areaIndex', [1, 2, 3]);
p.addParameter('eccLo', 1.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('eccHi', 7.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('nonVisual', 0);
p.addParameter('prfROI', 0);
p.addParameter('polarLo', 0.0);
p.addParameter('polarHi', 0.0);

% Parse augements
parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccLo = p.Results.eccLo;
eccHi = p.Results.eccHi;
nonVisual = p.Results.nonVisual;
prfROI = p.Results.prfROI;
polarLo = p.Results.polarLo;
polarHi = p.Results.polarHi;

if nonVisual == 0
    if prfROI == 0
        % Select voxels from visual area based on ROI
        [eccen, varea, ~, ~] = load_map(sub_name);

        % select visual area and eccentricity
        [roi_mask, ~] = ecc_mask(varea, eccen, areaIndex, eccLo, eccHi);

        % visual area and ecc label
        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);

    elseif prfROI == 1
        % Define ROI using pRF size information
        [eccen, varea, sigma, ~] = load_map(sub_name);
        roi_mask = boolean(zeros(size(varea)));

        prfLo = eccen - 2 * sigma;

        % select visual area
        for idx = areaIndex
            roi_mask = roi_mask | varea == idx;
            fprintf('V%d ', idx)
        end
        fprintf('# of Voxel: %d \n', sum(roi_mask));
        nVoxel = sum(roi_mask);

        roi_mask  = roi_mask & (prfLo > eccLo) & (prfLo < eccHi);
        fprintf('pRF mask: %d / %d selected \n', sum(roi_mask), nVoxel);

        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);

    elseif prfROI == 2
        % Define ROI using pRF size information
        [eccen, varea, sigma, ~] = load_map(sub_name);
        roi_mask = boolean(zeros(size(varea)));

        prfHi = eccen + 2 * sigma;

        % select visual area
        for idx = areaIndex
            roi_mask = roi_mask | varea == idx;
            fprintf('V%d ', idx)
        end
        fprintf('# of Voxel: %d \n', sum(roi_mask));
        nVoxel = sum(roi_mask);

        roi_mask  = roi_mask & (prfHi > eccLo) & (prfHi < eccHi);
        fprintf('pRF mask: %d / %d selected \n', sum(roi_mask), nVoxel);

        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);

    elseif prfROI == 3
        % Polar angle ROI
        % ecc ROI [1, 7] degree

        % Select voxels from visual area based on ROI
        [eccen, varea, ~, angle] = load_map(sub_name);
        
        % select visual area and eccentricity
        eccLo = 1; eccHi = 7;
        [roi_mask, nVoxel] = ecc_mask(varea, eccen, areaIndex, eccLo, eccHi);
        
        % apply polar angle map
        roi_mask = roi_mask & polar_mask(angle, polarLo, polarHi);
        fprintf('Polar Angle mask: %d / %d selected \n', sum(roi_mask), nVoxel);

        % visual area and ecc label
        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);

    elseif prfROI == 4
        % PolarPostiveTangent ROI
        % Select voxels from visual area based on ROI
        [eccen, varea, ~, angle] = load_map(sub_name);

        % select visual area and eccentricity
        eccLo = 1; eccHi = 7;
        [roi_mask, nVoxel] = ecc_mask(varea, eccen, areaIndex, eccLo, eccHi);

        % polar angle
        polarLo = 5; polarHi = 65;
        mask = polar_mask(angle, polarLo, polarHi);

        polarLo = 95; polarHi = 155;
        mask = mask | polar_mask(angle, polarLo, polarHi);

        roi_mask = roi_mask & (~mask);
        fprintf('Polar Angle mask: %d / %d selected \n', sum(roi_mask), nVoxel);

        % visual area and ecc label
        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);

    elseif prfROI == 5
        % PolarNegativeTangent ROI
        % Select voxels from visual area based on ROI
        [eccen, varea, ~, angle] = load_map(sub_name);

        % select visual area and eccentricity
        eccLo = 1; eccHi = 7;
        [roi_mask, nVoxel] = ecc_mask(varea, eccen, areaIndex, eccLo, eccHi);

        % polar angle
        polarLo = 115; polarHi = 175;
        mask = polar_mask(angle, polarLo, polarHi);

        polarLo = 25; polarHi = 85;
        mask = mask | polar_mask(angle, polarLo, polarHi);

        roi_mask = roi_mask & (~mask);
        fprintf('Polar Angle mask: %d / %d selected \n', sum(roi_mask), nVoxel);

        % visual area and ecc label
        v_label = varea(roi_mask);
        e_label = eccen(roi_mask);
    end

elseif nonVisual == 1
    % Return 1,000 voxel from non-visual area
    nVoxel = 1000;
    fprintf('Select %d Non-Visual Voxel \n', nVoxel);

    mask_path = '~/Data/fMRI/ORNT/visual_areas_mask.nii';
    visual = cifti_read(mask_path);
    visual = visual.cdata;

    rng(0);
    nonIndex = 1:length(visual);
    nonIndex = nonIndex(~visual);
    nonIndex = nonIndex(randperm(length(nonIndex)));

    roi_mask = boolean(zeros(size(visual)));
    roi_mask(nonIndex(1:nVoxel)) = 1;

    v_label = '';
    e_label = '';

elseif nonVisual == 2
    % Return M1 (motor) cortex indices
    atlas_path = '~/Data/fMRI/ORNT/cortical_areas.nii';
    atlas = cifti_read(atlas_path);
    index = atlas.cdata;
    roi_mask = boolean(zeros(size(index)));

    % Area 4 (primary motor cortex)
    % R_4 = 8, L_4 = 188
    target = [8, 188];
    for t = target
        roi_mask(index == t) = 1;
    end

    fprintf('Select %d M1 (Motor) Voxel \n', sum(roi_mask));

    v_label = '';
    e_label = '';

elseif nonVisual == 3
    % Return auditory cortex indices
    atlas_path = '~/Data/fMRI/ORNT/cortical_areas.nii';
    atlas = cifti_read(atlas_path);
    index = atlas.cdata;
    roi_mask = boolean(zeros(size(index)));

    % R_A1 = 24, L_A1 = 204
    % R_Belt: 124, 173, 174
    % L_Belt: 304, 353, 354
    target = [24, 204, 124, 173, 174, 304, 353, 354];
    for t = target
        roi_mask(index == t) = 1;
    end

    fprintf('Select %d Auditory Cortex Voxel \n', sum(roi_mask));

    v_label = '';
    e_label = '';

else
    fprintf('Non Visual Index Not Valid \n');
end

end
