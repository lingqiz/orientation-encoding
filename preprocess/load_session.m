function data = load_session(sub_name, acq_type, acq_idx, icafix)

% Load data from a single scan session
% tbUseProject('forwardModel') for setup
addpath('cifti-matlab');

% Single scan session: 91282 grayordinate * nAcq * 275 TRs
% 220 sec / acquisition * n acquisitions
base_dir = '~/Data/fMRI';
data_dir = fullfile(base_dir, sub_name, acq_type);

base = 'func-%02d_Atlas_hp2000_clean.dtseries.nii';
all_ts = cell(1, length(acq_idx));

counter = 1;
if icafix
    % Load ICAFIX data
    for idx = acq_idx
        fl = sprintf(base, idx);
        full_path = fullfile(data_dir, 'ICAFIX', fl);
        ts = cifti_read(full_path);
        ts = ts.cdata;
        
        % Convert to percent change
        meanVec = mean(ts, 2);
        ts = 100 * ((ts - meanVec) ./ meanVec);
        
        % Z-score normalization
        meanVec = mean(ts, 2);
        stdVec = std(ts, 0, 2);
        ts = (ts - meanVec) ./ stdVec;
        
        % Add to ts list
        all_ts{counter} = ts;
        counter = counter + 1;
    end    
else
    % Load motion regressed data
    for idx = acq_idx
        fl = sprintf(base, idx);
        ts = cifti_read(fullfile(data_dir, fl));
        
        all_ts{counter} = ts.cdata;
        counter = counter + 1;
    end    
end

data = cat(2, all_ts{:});

end