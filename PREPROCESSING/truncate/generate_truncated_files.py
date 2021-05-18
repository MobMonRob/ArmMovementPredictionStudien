import os

from ArmMovementPredictionStudien.PREPROCESSING.truncate.truncate_data_utils import truncate_dataset_position
from ArmMovementPredictionStudien.PREPROCESSING.utils.utils import open_dataset_pandas

directory = "../../DATA/2_smoothed/"

for file in os.listdir(directory):
    try:
        truncated_dataset, th = truncate_dataset_position(file, joint_type='w', threshold=0.01, directory=directory)
    except:
        print(f"Truncation not possible, {file} will be copied only")
        truncated_dataset = open_dataset_pandas(file, directory)
    new_filename = "../../DATA/3_truncated/" + file.replace("smoothed", "truncated")
    truncated_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
