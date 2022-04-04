% Simultaneous estimate of both the HRF function 
% and the beta weights of stimulus presentation

%% Load data from a single scan session
addpath('cifti-matlab');

% single scan: 91282 grayordinate * 2750 TRs (2200 sec)
% 220 sec / acquisition * 10 acquisitions
base_dir = '~/Data/fMRI';
sub_name = 'HERO_LZ';
acq_type = 'NeuralCoding01';

ts_pt1 = cifti_read('ICAFIX_pt1_clean.dtseries.nii');
ts_pt2 = cifti_read('ICAFIX_pt2_clean.dtseries.nii');
data = {[ts_pt1.cdata, ts_pt2.cdata]};

%% Set up stim regressors
% single scan structure 
% 12.5 s * 2 blank (begin/end)
% (1.5 s stim + 3.5 ISI) * 39 presentation
% attention event
tr = 0.5; nTR = 2200 / 0.5;
stimTime = (1:nTR )* tr;

% nAcq = 10; nStim = 39;
% 
% stimDur = 1.5;
% stimDly = 3.5;
% blankDur = 12.5;
% 
% stim = zeros(nStim * nAcq, nTR);
% t = 0; stimIdx = 0;
% 
% for idx = 1:nAcq
%     t = t + blankDur; 
%     for idy = 1:nStim
%         stimIdx = stimIdx + 1;
%         
%         % TR begin index
%         trStart = t / 0.8;
%         t = t + 1.5;
%         
%         % TR end index 
%         trEnd = t / 0.8;
%         
%         % Set stimulus regressor values
%         stim(stimIdx, ceil(trStart) : floor(trEnd)) = 1.0;
%         stim(stimIdx, floor(trStart)) = trStart - floor(trStart);
%         stim(stimIdx, ceil(trEnd)) = ceil(trEnd) - trEnd;
%                 
%         t = t + 3.5;
%     end
%     t = t + blankDur;
% end
