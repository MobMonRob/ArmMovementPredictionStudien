import os
import matplotlib.pyplot as plt

from ArmMovementPredictionStudien.Preprocessing.truncate.truncate_data_utils import find_maximum_velocity_of_trajectory
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
import pandas as pd

from ArmMovementPredictionStudien.Preprocessing.utils.velocity import generate_velocity_dataframe

ROOT_DIR = os.path.dirname(__file__) + "/../../"

base_directory = ROOT_DIR + "DATA/"
raw_directory = base_directory + "0_raw/"
truncated_directory = base_directory + "3_truncated/"

filelist_raw = os.listdir(raw_directory)
filelist_truncated = os.listdir(truncated_directory)

length_raw = {}
max_velocity_raw = {}
for file in filelist_raw:
    raw_df = open_dataset_pandas(file, raw_directory)
    length_raw.update({file: len(raw_df)})
    velocity_raw_df = generate_velocity_dataframe(file, raw_directory)
    max_v = find_maximum_velocity_of_trajectory(velocity_raw_df)
    max_velocity_raw.update({file: max_v.iloc[0, 1]})

length_truncated = {}
max_velocity_truncated = {}
for file in filelist_truncated:
    truncated_df = open_dataset_pandas(file, truncated_directory)
    length_truncated.update({file: len(truncated_df)})
    try:
        velocity_truncated_df = generate_velocity_dataframe(file, truncated_directory)
        max_v = find_maximum_velocity_of_trajectory(velocity_truncated_df)
        max_velocity_truncated.update({file: max_v.iloc[0, 1]})
        if max_v.iloc[0, 1] > 1000:
            print(f"{file}; v_max: {max_v.iloc[0, 1]}")
    except TypeError:
        print(file)

fig, ax = plt.subplots(2, 2)
pd.DataFrame({"length_raw": list(length_raw.values())}).hist(ax=ax[0, 0], bins=20)
pd.DataFrame({"length_truncated": list(length_truncated.values())}).hist(ax=ax[0, 1], bins=20)
pd.DataFrame({"max_velocity_raw": list(max_velocity_raw.values())}).hist(ax=ax[1, 0], bins=40)
pd.DataFrame({"max_velocity_truncated": list(max_velocity_truncated.values())}).hist(ax=ax[1, 1], bins=40)

plt.show()
