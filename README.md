# ArmMovementPredictionStudien

Arm movement prediction for collaborative robotics based on neuronal networks.

## Usage

- ...

## Project structure

### DATA

This folder contains the processed data. For each preprocessing phase of the pipeline, there is a folder that contains all files in the corresponding processing state.*98_broken_prefiltered* contains all files sorted out in prefiltering, *99_broken* all files sorted out in filtering. *71_broken* contains all files sorted out by a specific metric during filtering, the metric can be set in jupyter notebook.

### MJM

### ML

This folder contains all Machine Learning related files.

- **ML.ipynb**: Jupyter notebook for Machine Learning  with python code for training and visualisation of training results.
- **models_overview.csv**: Contains all tested ML configurations (different hyper parameters, input sizes, architectures, ...), for each configuration there is a corresponding JSON-file in **/model_configurations** to import the configuration.
- **Overview.xlsx**: Excel sheet to compare training results of different configurations.
- **/predictions**: Contains CSVs with real and predicted endpoints (by a particular trained model)

### PREPROCESSING

#### visualisation

- **animateData(csvNumber, phaseNumber, side)**: Animates hand movement to estimate velocity profile
- **drawAllBrokenFiles(max)**: Visualizes files sorted out in filtering with reasons
- **drawAllFiles(phaseNumber, side, bodyPart)**: Visualizes all trajectories of a given phase, side and bodypart
- **drawData(csvNumber,phaseNumber)**: Visualizes one dataset at a given phase
