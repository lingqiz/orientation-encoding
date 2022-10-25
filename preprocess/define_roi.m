function [roi_mask, v_label, e_label] = define_roi(sub_name, varargin)

p = inputParser;

% Default ROI: V1 - V3 area, 10 degree eccentricity, r-square > 0.10
p.addParameter('areaIndex', [1, 2, 3]);
p.addParameter('eccThreshold', 10.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('rsqrThreshold', 0.10, @(x)(isnumeric(x) && numel(x) == 1));

parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccThreshold = p.Results.eccThreshold;
rsqrThreshold = p.Results.rsqrThreshold;

[eccen, varea, rsqr] = load_map(sub_name);
roi_mask = boolean(zeros(size(varea)));

% select visual area
for idx = areaIndex
    roi_mask = roi_mask | varea == idx;
    fprintf('V%d ', idx)
end
fprintf('# of Voxel: %d \n', sum(roi_mask));
nVoxel = sum(roi_mask);

% apply eccentricity map
roi_mask  = roi_mask & (eccen > 0) & (eccen <= eccThreshold);
fprintf('Eccen mask: %d / %d selected \n', sum(roi_mask), nVoxel);
nVoxel = sum(roi_mask);

% apply rsquare map
roi_mask  = roi_mask & (rsqr >= rsqrThreshold);
fprintf('Rsqur mask: %d / %d selected \n', sum(roi_mask), nVoxel);

% visual area and ecc label
v_label = varea(roi_mask);
e_label = eccen(roi_mask);

end
