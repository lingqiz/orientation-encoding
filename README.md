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
- pRF session (flywheel): Hcp-Struct, Hcp-Func, ICAFIX, Forward Model, Bayes pRF
- Stimulus session:
ts_filter.m (percent change, motion regression, detrend, z-score)
icafix + z-score normalization