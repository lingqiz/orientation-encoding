function [eccen, varea, rsqr] = load_map(sub_name)

% Data directories
base_dir = '~/Data/fMRI/ORNT';
acq_type = 'cifti_maps';
data_dir = fullfile(base_dir, sub_name, acq_type);

% Load cifti data
eccen_fl = strcat(sub_name, '_inferred_eccen.dtseries.nii');
varea_fl = strcat(sub_name, '_inferred_varea.dtseries.nii');
rsqr_fl = strcat(sub_name, '_R2_map.dtseries.nii');

eccen = cifti_read(fullfile(data_dir, eccen_fl));
varea = cifti_read(fullfile(data_dir, varea_fl));
rsqr = cifti_read(fullfile(data_dir, rsqr_fl));

% Return eccen and varea maps
eccen = eccen.cdata;
varea = varea.cdata;
rsqr = rsqr.cdata;

end