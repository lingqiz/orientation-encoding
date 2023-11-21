# Orientation-Encode

### Instruction
Each subject should be assigned a unique `subject_ID`.
- fMRI session: `python3 main.py subject_ID`.
The code automatically tracks the acquisition number.
- behavioral session: (switch to the behavior branch)
`python3 main.py subject_ID`.
- See `analysisTilt.m` for analysis of behavioral data.

### Dependencies
- [PsychoPy](https://www.psychopy.org/)
- [cifti-matlab](https://github.com/Washington-University/cifti-matlab)

### Pre-processing Note
- pRF session (flywheel): HcpStruct - HcpFunc - ICAFIX - [ForwardModel](https://github.com/gkaguirrelab/forwardModel) - [BayesPRF](https://elifesciences.org/articles/40224)  
See here for information regarding the [HCP pre-processing pipeline](https://github.com/Washington-University/HCPpipelines)  

Note: To calculate the magnification factor, use   
`tbUse('gkaModelEye');
open d003_spectacleMag`

- Stimulus session:    
  `avg_resp.m` (high-pass filter, motion regression, align time course after each stimulus presentation, z-score across corresponding time points, average within a time window [4s, 8s])  

  *(not in use)* `ts_filter.m` (high-pass filter, motion regression, z-score within each run)  
  Next, run `glm_fit.m` (nonlinear fitting of GLM + HRF based on [ForwardModel](https://github.com/gkaguirrelab/forwardModel))  
