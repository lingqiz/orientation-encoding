# Orientation Encoding in the Tilt Illusion
**The tilt illusion arises from an efficient reallocation of neural coding resources at the contextual boundary**  
Ling-Qi Zhang, Jiang Mao, Geoffrey K Aguirre, and Alan A Stocker  
https://www.biorxiv.org/content/10.1101/2024.09.17.613538v1

---

## Dependencies
- [PsychoPy](https://www.psychopy.org/) (For running experiment, not required for data analysis code)
- [cifti-matlab](https://github.com/Washington-University/cifti-matlab) (For fMRI data preprocessing)
- Use `pip install -r requirements.txt` to install other Python dependencies before running our analysis pipeline.

---

## Data Analysis
The scripts below outline our data analysis methods.   
Access and download our pre-processed fMRI data from [OSF](https://osf.io/9uqbd/).  
After downloading, unzip the files and place each subject’s data under `~/Data/fMRI/ORNT/`.

### Behavioral data analysis
- See `script/combineSub.m` for analysis of behavioral data. 
- `script/behaviorPlot.m` performs bootstrapping.

### Neural data analysis 
- Use `preprocess/run_roi.m` to extract the voxel activity pattern from the ROI(s) of interest.
- See `script/decoding.ipynb` for an example of running orientation decoding.
- See `script/fisher.ipynb` for an example of extracting the neural FI for the combined subject in the baseline condition.
- See `cv_decode` from `analysis/ornt.py` to perform cross-validated decoding analysis.
- Please refer to `analysis/encode.py` for the code of the forward encoding model, model fitting procedure, etc.

---

## Run Experiment
The following information is for running the experiment and preprocessing the fMRI data.  

### PsychoPy
Each subject should be assigned a unique `subject_ID`.
- fMRI session: `python3 run_exp.py subject_ID`.
The code automatically tracks the acquisition number and conditions across runs.

### Pre-processing (flywheel)
- Retinotopic mapping: HcpStruct - HcpFunc - ICAFIX - [ForwardModel](https://github.com/gkaguirrelab/forwardModel) - [BayesPRF](https://elifesciences.org/articles/40224)  
See here for information regarding the [HCP pre-processing pipeline](https://github.com/Washington-University/HCPpipelines)  

Note: To calculate the magnification factor, use   
`tbUse('gkaModelEye');
open d003_spectacleMag`

- Stimulus session: (HcpStruct) - HcpFunc  
  `avg_resp.m` (high-pass filter, motion regression, align time course after each stimulus presentation, z-score across corresponding time points, average within a time window [4s, 8s]) 
