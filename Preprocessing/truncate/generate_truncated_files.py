import os

from ArmMovementPredictionStudien.Preprocessing.truncate.truncate_data_utils import truncate_dataset_position, \
    truncate_dataset_position_with_acceleration
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
import numpy as np

directory = "../../DATA/2_smoothed/"

for file in os.listdir(directory):
    try:
        # i = 0.01
        truncated_dataset, th = truncate_dataset_position(file, joint_type='w', threshold=0.01, directory=directory)
        # for i in np.arange(0.02, 0.31, 0.01):
        #     if len(truncated_dataset) > 150:
        #         truncated_dataset = truncate_dataset_position(file, joint_type='w', threshold=i, directory=directory)
        #     else:
        #         break
        # if len(truncated_dataset) > 150:
        #     print(f"{file};{i};{len(truncated_dataset)}")
        # #else:
        #     print(f"{file};{i-0.01};{len(truncated_dataset)}")
    except:
        print(f"Truncation not possible, {file} will be copied only")
        truncated_dataset = open_dataset_pandas(file, directory)
    new_filename = "../../DATA/3_truncated/" + file.replace("smoothed", "truncated")
    truncated_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')

#
# for file in os.listdir(directory):
#     try:
#         truncated_dataset = \
#             truncate_dataset_position_with_acceleration(file, joint_type='w', threshold=0.01, directory=directory)
#     except:
#         print(f"Truncation not possible, {file} will be copied only")
#         truncated_dataset = open_dataset_pandas(file, directory)
#     new_filename = "../../DATA/3_truncated/" + file.replace("smoothed", "truncated")
#     truncated_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
