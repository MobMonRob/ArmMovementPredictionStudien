# ArmMovementPredictionStudien

Arm movement prediction for collaborative robotics based on neuronal networks.

## Usage

- ...

## Project structure

### DATA

This folder contains the processed data. For each preprocessing phase of the pipeline, there is a folder that contains all files in the corresponding processing state.*98_broken_prefiltered* contains all files sorted out in prefiltering, *99_broken* all files sorted out in filtering. *71_broken* contains all files sorted out by a specific metric during filtering, the metric can be set in jupyter notebook.

### MJM
- contains script to model trajectories according to several minimum jerk models
- contains octave script to visualise prediction
- contains folder for files with coordinates of predicted trajectories

### ML

This folder contains all Machine Learning related files.

- **ML.ipynb**: Jupyter notebook for Machine Learning  with python code for training and visualisation of training results.
- **models_overview.csv**: Contains all tested ML configurations (different hyper parameters, input sizes, architectures, ...), for each configuration there is a corresponding JSON-file in **/model_configurations** to import the configuration.
- **Overview.xlsx**: Excel sheet to compare training results of different configurations.
- **/predictions**: Contains CSVs with real and predicted endpoints (by a particular trained model)

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
- contains python and octave scripts to visualise data for certain purposes

- **animateData(csvNumber, phaseNumber, side)**: Animates hand movement to estimate velocity profile
- **drawAllBrokenFiles(max)**: Visualizes files sorted out in filtering with reasons
- **drawAllFiles(phaseNumber, side, bodyPart)**: Visualizes all trajectories of a given phase, side and bodypart
- **drawData(csvNumber,phaseNumber)**: Visualizes one dataset at a given phase
- **drawMirrored(csvNumber, origOrRight)**: Visualizes mirrored files in comparison to either original trajectory or according other body half
- **drawPoints(side)**: Visualizes all endpoints at given body half
- **drawPredictions()**: Visualizes real endpoints compared to according predicted ones
- **drawRotated(csvNumber)**: Visualizes rotated trajectory
