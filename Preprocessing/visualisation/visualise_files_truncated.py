import os

from ArmMovementPredictionStudien.Preprocessing.utils.velocity import generate_velocity_dataframe, \
    calculate_velocity_of_trajectory
import matplotlib.pyplot as plt

file_selection = "20200423327_raw_L.csv"

ROOT_DIR = os.path.dirname(__file__) + "/../../"

base_directory = ROOT_DIR + "DATA/"
raw_directory = base_directory + "0_raw/"
interpolated_directory = base_directory + "3_truncated/"
smoothed_directory = base_directory + "3_truncated_1/"
truncated_directory = base_directory + "3_truncated_2/"

if file_selection.find("_") != 11:
    raise Exception("Wrong filename")
file_id = file_selection[0:11]
file_left_right = file_selection[-5]
file_extension = ".csv"

filename_raw = file_id + "_raw_" + file_left_right + file_extension
filename_interpolated = file_id + "_truncated_" + file_left_right + file_extension
filename_smoothed = file_id + "_truncated_" + file_left_right + file_extension
filename_truncated = file_id + "_truncated_" + file_left_right + file_extension

dataset_velocity_raw = \
    calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_raw, raw_directory, False))
dataset_velocity_interpolated = \
    calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_interpolated, interpolated_directory, False))
dataset_velocity_smoothed = \
    calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_smoothed, smoothed_directory, False))
dataset_velocity_truncated = \
    calculate_velocity_of_trajectory(generate_velocity_dataframe(filename_truncated, truncated_directory, False))

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(range(0, len(dataset_velocity_raw)), dataset_velocity_raw)
axs[0, 0].set_title(filename_raw)
axs[0, 1].plot(range(0, len(dataset_velocity_interpolated)), dataset_velocity_interpolated, 'tab:orange')
axs[0, 1].set_title("Truncated recursive; 150; max_threshold 1.0")
axs[1, 0].plot(range(0, len(dataset_velocity_smoothed)), dataset_velocity_smoothed, 'tab:green')
axs[1, 0].set_title("Truncated with acceleration; threshold 1.0")
axs[1, 1].plot(range(0, len(dataset_velocity_truncated)), dataset_velocity_truncated, 'tab:red')
axs[1, 1].set_title("Truncated iterative; 150; max_threshold 0.3")

plt.show()
