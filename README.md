# Orientation Encoding in Tilt Illusion

## Dependencies
- [PsychoPy](https://www.psychopy.org/) (For experiment)
- [cifti-matlab](https://github.com/Washington-University/cifti-matlab) (For fMRI data preprocessing)
- Use `pip install -r requirements.txt` before running our analysis pipeline. 

## Run Experiment
The following information is for running the experiment and preprocessing the fMRI data.  

### PsychoPy
Each subject should be assigned a unique `subject_ID`.
- fMRI session: `python3 main.py subject_ID`.
The code automatically tracks the acquisition number.

### Pre-processing (flywheel)
- Retinotopic mapping: HcpStruct - HcpFunc - ICAFIX - [ForwardModel](https://github.com/gkaguirrelab/forwardModel) - [BayesPRF](https://elifesciences.org/articles/40224)  
See here for information regarding the [HCP pre-processing pipeline](https://github.com/Washington-University/HCPpipelines)  

Note: To calculate the magnification factor, use   
`tbUse('gkaModelEye');
open d003_spectacleMag`

- Stimulus session: (HcpStruct) - HcpFunc  
  `avg_resp.m` (high-pass filter, motion regression, align time course after each stimulus presentation, z-score across corresponding time points, average within a time window [4s, 8s]) 

## Data Analysis
The scripts below outline our data analysis methods.  
Use [Link to OSF] to access and download our pre-processed fMRI data. 

### Behavioral data analysis
- See `script/combineSub.m` for analysis of behavioral data. 
- `script/behaviorPlot.m` performs bootstrapping.

### Neural data analysis 
1. Use `preprocess/run_roi.m` to extract the voxel activity pattern from the ROI(s) of interest.
2. Use `cv_decode` from `analysis/ornt.py` to perform cross-validated decoding analysis.
3. Use `llhd_derivative` from `analysis/ornt.py` to compute the second derivatives of likelihood, based on which the neural Fisher information is computed. 

---

- See `script/decoding.ipynb` for an example of running orientation decoding.
- See `script/fisher.ipynb` for an example of extracting the neural FI for the combined subject in the baseline condition.
- Please refer to `analysis/encode.py` for the code of the forward encoding model, model fitting procedure, etc.  
