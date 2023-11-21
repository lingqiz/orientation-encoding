function beta_sub(sub_name, varargin)

p = inputParser;

% Define ROI: visual area index and eccentricity
% Stimulus: 0 - 1.5 deg; 1.5 - 7 deg; 7 - 12.5 deg

% Area - Index Correspondence
% {1:  'V1',   2: 'V2',  3: 'V3',  4: 'hV4',  5: 'VO1', 6:  'VO2',  
% 7: 'LO1', 8: 'LO2', 9: 'TO1', 10: 'TO2', 11: 'V3b', 12: 'V3a'}

% Default ROI: V1 - V3 area, foeval - 7.0 degree eccentricity
p.addParameter('areaIndex', [1, 2, 3]);
p.addParameter('eccLo', 1.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('eccHi', 7.0, @(x)(isnumeric(x) && numel(x) == 1));
p.addParameter('cutoffT', 150, @(x)(isnumeric(x) && numel(x) == 1))

parse(p, varargin{:});
areaIndex = p.Results.areaIndex;
eccLo = p.Results.eccLo;
eccHi = p.Results.eccHi;
cutOffT = p.Results.cutoffT;

% Extract "beta" response from time series

end