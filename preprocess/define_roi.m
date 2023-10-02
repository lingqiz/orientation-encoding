function [roi_mask, v_label, e_label] = define_roi(sub_name, varargin)

p = inputParser;

% Default ROI: V1 - V3 area, 1.5 - 7.5 degree eccentricity
p.addParameter('areaIndex', [1, 2, 3]);
p.addParameter('eccLo', 1.5, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('eccHi', 7.5, @(x)(isnumeric(x) && numel(x) == 1));

parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccLo = p.Results.eccLo;
eccHi = p.Results.eccHi;

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
