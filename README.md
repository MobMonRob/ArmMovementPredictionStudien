# ArmMovementPredictionStudien

Arm movement prediction for collaborative robotics based on neuronal networks.

## Usage

- ...

## Project structure

### DATA

### MJM
- contains script to model trajectories according to several minimum jerk models
- contains octave script to visualise prediction
- contains folder for files with coordinates of predicted trajectories

### ML

### PREPROCESSING
This folder contains everything necessary for preprocessing of recorded data to train the ML-model. Use the Jupyter Notebook preprocessing_pipeline.ipynb to run the complete preprocessing procedure.

#### endpoints_comparison
- contains script to generate files with endpoints of all trajectories on a certain date
- contains datasets with endpoints sorted by date
#### manual_labeling
- contains script to label tractories 'good' or 'bad' manually
#### mirror_left_files
- contains scripts and utils for mirroring files of left body half
#### smooth
- contains scripts and utils to smooth trajectories
#### truncate
- contains scripts and utils to truncate trajectories
#### utils
- contains scripts to open files in python or calculate velocities
#### visualisation
- comtains python and octave scripts to visualise data for certain purposes