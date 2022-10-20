# Orientation-Encode
Code for running the experiment and data analysis pipeline for orientation encoding experiment with tilt illusion.

### Instruction
Each subject should be assigned a unique `subject_ID`.
- fMRI session: `python3 main_psv.py subject_ID`.
The code automatically tracks the acquisition number.
- behavioral session: (switch to the behavior branch)
`python3 main.py subject_ID`.

### Dependencies
- [PsychoPy](https://www.psychopy.org/)
- [cifti-matlab](https://github.com/Washington-University/cifti-matlab)

### Pre-processing Note
- pRF session (flywheel): HcpStruct - HcpFunc - ICAFIX - [ForwardModel](https://github.com/gkaguirrelab/forwardModel) - [BayesPRF](https://elifesciences.org/articles/40224)  
See here for information regarding the [HCP pre-processing pipeline](https://github.com/Washington-University/HCPpipelines)  
Alternatively, skip ICAFIX and use `ts_filter.py`
- Stimulus session:  
Pre-process  
*(option 1)* `ts_filter.m` (high-pass filter, motion regression, z-score within each run)  
*(option 2)* ICAFIX, percent change, z-score  

  Run `load_atten.py` to extra the attentional event data into `.mat` file format  
  Next, run `glm_fit.m` (nonlinear fitting of GLM + HRF based on [ForwardModel](https://github.com/gkaguirrelab/forwardModel))    
  
  *(option 3)* `avg_resp.m` (high-pass filter, motion regression, align time course after each stimulus presentation, z-score across corresponding time points, average within a time window [4s, 8s])  
