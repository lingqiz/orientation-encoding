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
p.addParameter('nonVisual', false);

parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccLo = p.Results.eccLo;
eccHi = p.Results.eccHi;
nonVisual = p.Results.nonVisual;

if nonVisual
    % return 1,000 voxel from non-visual area
    nVoxel = 1000;
    fprintf('Select %d Non-Visual Voxel \n', nVoxel);
    
    mask_path = '~/Data/fMRI/ORNT/visual_areas_mask.nii';
    visual = cifti_read(mask_path);
    visual = visual.cdata;

    rng("default");
    nonIndex = 1:length(visual);
    nonIndex = nonIndex(~visual);
    nonIndex = nonIndex(randperm(length(nonIndex)));

    roi_mask = boolean(zeros(size(visual)));
    roi_mask(nonIndex(1:nVoxel)) = 1;
    v_label = '';
    e_label = '';

else
    [eccen, varea, ~] = load_map(sub_name);
    roi_mask = boolean(zeros(size(varea)));

    % select visual area
    for idx = areaIndex
        roi_mask = roi_mask | varea == idx;
        fprintf('V%d ', idx)
    end
    fprintf('# of Voxel: %d \n', sum(roi_mask));
    nVoxel = sum(roi_mask);

    % apply eccentricity map
    roi_mask  = roi_mask & (eccen > eccLo) & (eccen <= eccHi);
    fprintf('Eccen mask: %d / %d selected \n', sum(roi_mask), nVoxel);

    % visual area and ecc label
    v_label = varea(roi_mask);
    e_label = eccen(roi_mask);
end

end
