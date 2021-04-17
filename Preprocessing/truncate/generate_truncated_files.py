import os

from ArmMovementPredictionStudien.Preprocessing.truncate.truncate_data_utils import truncate_dataset_position
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas

directory = "../../DATA/2_smoothed/"

for file in os.listdir(directory):
    try:
        truncated_dataset = truncate_dataset_position(file, joint_type='w', threshold=0.01, directory=directory)
        for i in [0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]:
            if len(truncated_dataset) > 150:
                truncated_dataset = truncate_dataset_position(file, joint_type='w', threshold=i, directory=directory)
    except:
        print(f"Truncation not possible, {file} will be copied only")
        truncated_dataset = open_dataset_pandas(file, directory)
    new_filename = "../../DATA/3_truncated/" + file.replace("smoothed", "truncated")
    truncated_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
