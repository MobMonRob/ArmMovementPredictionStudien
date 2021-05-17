import os

from ArmMovementPredictionStudien.Preprocessing.utils.velocity import generate_velocity_dataframe, \
    calculate_velocity_of_trajectory
import matplotlib.pyplot as plt
from random import shuffle

pick_random_file = False
file_selection = "20200423306_raw_R.csv "
file_selection = file_selection.strip()

ROOT_DIR = os.path.dirname(__file__) + "/../../"

base_directory = ROOT_DIR + "DATA/"
raw_directory = base_directory + "0_raw/"
filtered_directory = base_directory + "6_filtered/"
broken_directory = base_directory + "99_broken/"
broken_prefiltered_directory = base_directory + "98_broken_prefiltered/"

if pick_random_file:
    all_files = os.listdir(raw_directory)
    shuffle(all_files)
    file_selection = all_files[0]

if file_selection.find("_") != 11:
    raise Exception("Wrong filename")
file_id = file_selection[0:11]
file_left_right = file_selection[-5]
file_extension = ".csv"

filename_raw = file_id + "_raw_" + file_left_right + file_extension
filename_filtered = file_id + "_filtered_" + file_left_right + file_extension
filename_broken = file_id + "_broken_" + file_left_right + file_extension
filename_broken_prefiltered = file_id + "_broken_prefiltered_" + file_left_right + file_extension

files_filtered = os.listdir(filtered_directory)
files_broken = os.listdir(broken_directory)
files_broken_prefiltered = os.listdir(broken_prefiltered_directory)

dataset_velocity_raw = \
    calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_raw, raw_directory, False))
dataset_velocity_filtered = {}
dataset_velocity_broken = {}
dataset_velocity_broken_prefiltered = {}

if filename_filtered in files_filtered:
    filtered = 'filtered'
    dataset_velocity_filtered = \
        calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_filtered, filtered_directory, False))
elif filename_broken in files_broken:
    filtered = 'broken'
    dataset_velocity_broken = \
        calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_broken, broken_directory, False))
elif filename_broken_prefiltered in files_broken_prefiltered:
    filtered = 'broken_prefiltered'
    dataset_velocity_broken_prefiltered = \
        calculate_velocity_of_trajectory(
            generate_velocity_dataframe(filename_broken_prefiltered, broken_prefiltered_directory, False))
else:
    raise Exception(f"File '{filename_raw}' seems not to exist.")

fig, axs = plt.subplots(1, 2)
axs[0].plot(range(0, len(dataset_velocity_raw)), dataset_velocity_raw)
axs[0].set_title(filename_raw)
if filtered == 'filtered':
    axs[1].plot(range(0, len(dataset_velocity_filtered)), dataset_velocity_filtered)
    axs[1].set_title(filename_filtered)
elif filtered == 'broken':
    axs[1].plot(range(0, len(dataset_velocity_broken)), dataset_velocity_broken)
    axs[1].set_title(filename_broken)
elif filtered == 'broken_prefiltered':
    axs[1].plot(range(0, len(dataset_velocity_broken_prefiltered)), dataset_velocity_broken_prefiltered)
    axs[1].set_title(filename_broken_prefiltered)

print(filename_raw)

plt.show()
