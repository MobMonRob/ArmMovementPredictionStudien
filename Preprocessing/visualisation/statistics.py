import os
import matplotlib.pyplot as plt
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
import pandas as pd

ROOT_DIR = os.path.dirname(__file__) + "/../../"

base_directory = ROOT_DIR + "DATA/"
raw_directory = base_directory + "0_raw/"
truncated_directory = base_directory + "3_truncated/"

filelist_raw = os.listdir(raw_directory)
filelist_truncated = os.listdir(truncated_directory)

length_raw = {}
for file in filelist_raw:
    raw_df = open_dataset_pandas(file, raw_directory)
    length_raw.update({file: len(raw_df)})

length_truncated = {}
for file in filelist_truncated:
    truncated_df = open_dataset_pandas(file, truncated_directory)
    length_truncated.update({file: len(truncated_df)})

fig, ax = plt.subplots(1, 2)
pd.DataFrame({"length_raw": list(length_raw.values())}).hist(ax=ax[0], bins=20)
pd.DataFrame({"length_truncated": list(length_truncated.values())}).hist(ax=ax[1], bins=20)

print(dict(filter(lambda e: e[1] > 160, length_truncated.items())))

plt.show()
