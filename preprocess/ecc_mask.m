function [mask, nVoxel] = ecc_mask(varea, eccen, areaIndex, eccLo, eccHi)

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

mask = roi_mask;

end