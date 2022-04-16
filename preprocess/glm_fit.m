function results = glm_fit(data, attEvent, base_idx, showPlot)

%% Default showPlot = True
if ~exist('showPlot', 'var')
    showPlot = true;
end

%% Set up stimulus regressors
tr = 0.8; dt = 0.5;
totalTime = size(data, 2) * tr;

acqLen = 220.0;
nAcq = totalTime / acqLen;
fprintf('Construct stim regressor for %d acquisitions \n', nAcq);

% Define a stimulus time axis with a different temporal support
stimTime = ((1:totalTime / dt) - 1) * dt;

% Single acquisition structure:
% 12.5 s * 2 blank (begin/end)
% (1.5 s Stim + 3.5 ISI) * 39 presentation
% attention event
nStim = 39;

stimDur = 1.5;
stimDly = 3.5;
blankDur = 12.5;

stim = zeros(nStim * nAcq, length(stimTime));
t = 0; stimIdx = 0;

% Calculate the time onset of each stimulus
for idx = 1:nAcq
    t = t + blankDur;
    for idy = 1:nStim
        stimIdx = stimIdx + 1;
        
        % Stim begin index
        idxStart = t / dt + 1;
        t = t + stimDur;
        % Stim end index
        idxEnd = t / dt;
        
        % Set stimulus regressor values
        stim(stimIdx, idxStart:idxEnd) = 1.0;
        t = t + stimDly;
    end
    t = t + blankDur;
end

%% Set up attent event regressor
if ~isempty(attEvent)
    % Plot attention RT
    if showPlot
        figure();
        allRT = cat(1, attEvent{:});
        histogram(allRT(:, 2)); box off;
        xlabel('Time'); ylabel('Count');
    end
    
    baseIdx = base_idx;
    eventRegressor = zeros(1, length(stimTime));
    
    for idx = 1:nAcq
        baseTime = (idx - 1) * acqLen;
        event = attEvent{baseIdx + idx};
        eventTime = baseTime + event(:, 1);
        
        for et = eventTime
            idxStart = ceil(et / dt) + 1;
            eventRegressor(idxStart) = 1.0;
        end
    end
    
    stim = [stim; eventRegressor];
end

%% Run GLM model with HRF fitting (mtSinai model class)
% polynom low frequency noise removal
modelOpts = {'polyDeg', 4};
results = forwardModel({data}, {stim}, tr, ...
    'modelClass', 'mtSinai', ...
    'stimTime', {stimTime'}, ...
    'modelOpts', modelOpts);

% return stim regressor
results.stimTime = stimTime;
results.stim = stim;

%% Post model fitting checks
if showPlot
    figure();
    histogram(results.R2); box off;
    xlabel('R2'); ylabel('Count');
    
    % Show the results figures
    figFields = fieldnames(results.figures);
    if ~isempty(figFields)
        for ii = 1:length(figFields)
            figHandle = struct2handle(results.figures.(figFields{ii}).hgS_070000,0,'convert');
            set(figHandle,'visible','on')
        end
    end
end

end
