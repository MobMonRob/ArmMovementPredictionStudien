import os
import matplotlib.pyplot as plt
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
import pandas as pd

ROOT_DIR = os.path.dirname(__file__) + "/../../"

base_directory = ROOT_DIR + "DATA/"
raw_directory = base_directory + "0_raw/"
truncated_directory = base_directory + "3_truncated/"
truncated_directory_1 = base_directory + "3_truncated_1/"
truncated_directory_2 = base_directory + "3_truncated_2/"

filelist_raw = os.listdir(raw_directory)
filelist_truncated = os.listdir(truncated_directory)
filelist_truncated_1 = os.listdir(truncated_directory_1)
filelist_truncated_2 = os.listdir(truncated_directory_2)

length_raw = {}
for file in filelist_raw:
    raw_df = open_dataset_pandas(file, raw_directory)
    length_raw.update({file: len(raw_df)})

length_truncated = {}
for file in filelist_truncated:
    truncated_df = open_dataset_pandas(file, truncated_directory)
    length_truncated.update({file: len(truncated_df)})

length_truncated_1 = {}
for file in filelist_truncated_1:
    truncated_df_1 = open_dataset_pandas(file, truncated_directory_1)
    length_truncated_1.update({file: len(truncated_df_1)})

length_truncated_2 = {}
for file in filelist_truncated_2:
    truncated_df_2 = open_dataset_pandas(file, truncated_directory_2)
    length_truncated_2.update({file: len(truncated_df_2)})

fig, ax = plt.subplots(1, 4)
pd.DataFrame({"length_raw": list(length_raw.values())}).hist(ax=ax[0], bins=20)
pd.DataFrame({"length_truncated": list(length_truncated.values())}).hist(ax=ax[1], bins=20)
pd.DataFrame({"length_truncated_1": list(length_truncated_1.values())}).hist(ax=ax[2], bins=20)
pd.DataFrame({"length_truncated_2": list(length_truncated_2.values())}).hist(ax=ax[3], bins=20)

print(dict(filter(lambda e: e[1] > 160, length_truncated.items())))
print(dict(filter(lambda e: e[1] > 160, length_truncated_1.items())))
print(dict(filter(lambda e: e[1] > 160, length_truncated_2.items())))

plt.show()
