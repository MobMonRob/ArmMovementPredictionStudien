# ArmMovementPredictionStudien

Arm movement prediction for collaborative robotics based on neuronal networks.

## Usage
### Setup
- Install Python 3.7
- Install [Jupyter Notebook](https://jupyter.org/install.html)
- Import the following libraries:
  - [Pandas](https://pandas.pydata.org/)
  - [Numpy](https://numpy.org/)
  - [Matplotlib](https://matplotlib.org/)
  - [Keras](https://keras.io/)
  - [Tensorflow](https://www.tensorflow.org/)
  - [Sklearn](https://scikit-learn.org/stable/)

### Run
You can run most of the phases of the data preprocessing pipeline ([`PREPROCESSING/preprocessing_pipeline.ipynb`](PREPROCESSING/preprocessing_pipeline.ipynb)) in your Jupyter Notebook by selecting the according cell and click "run". The phases which are not included (Truncation and Mirroring) are located in [`PREPROCESSING/truncate/generate_truncated_files.py`](PREPROCESSING/truncate/generate_truncated_files.py) and [`PREPROCESSING/mirror_left_files/mirror_files.py`](PREPROCESSING/mirror_left_files/mirror_files.py). You can run these scripts in your IDE.

The training for the Machine Learning model can be done in the Jupyter Notebook located in [`ML/ML.ipynb`](ML/ML.ipynb) and the prediction of the path in [`MJM/minimim_jerk.py`](MJM/minimum_jerk.py).

## Project structure

### DATA

This folder contains the processed data. For each preprocessing phase of the pipeline, there is a folder that contains all files in the corresponding processing state. *98_broken_prefiltered* contains all files sorted out in prefiltering, *99_broken* all files sorted out in filtering. *71_broken* contains all files sorted out by a specific metric during filtering, the metric can be set in jupyter notebook.

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
Contains script to generate files with endpoints of all trajectories on a certain date and datasets with endpoints sorted by date.
#### manual_labeling
Contains script to label tractories 'good' or 'bad' manually
#### mirror_left_files
Contains scripts and utils for mirroring files of left body half
#### smooth
Contains scripts and utils to smooth trajectories
#### truncate
Contains scripts and utils to truncate trajectories
#### utils
Contains scripts to open files in python or calculate velocities
#### visualisation
Contains python and octave scripts to visualise data for certain purposes

- **animateData(csvNumber, phaseNumber, side)**: Animates hand movement to estimate velocity profile
- **drawAllBrokenFiles(max)**: Visualizes files sorted out in filtering with reasons
- **drawAllFiles(phaseNumber, side, bodyPart)**: Visualizes all trajectories of a given phase, side and bodypart
- **drawData(csvNumber,phaseNumber)**: Visualizes one dataset at a given phase
- **drawMirrored(csvNumber, origOrRight)**: Visualizes mirrored files in comparison to either original trajectory or according other body half
- **drawPoints(side)**: Visualizes all endpoints at given body half
- **drawPredictions()**: Visualizes real endpoints compared to according predicted ones
- **drawRotated(csvNumber)**: Visualizes rotated trajectory
