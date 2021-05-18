import os

from numpy import sqrt
from numpy.random import shuffle

from ArmMovementPredictionStudien.PREPROCESSING.smooth import smooth_data_utils

import matplotlib.pyplot as plt

from ArmMovementPredictionStudien.PREPROCESSING.utils.velocity import calculate_velocity_vector_for_dataset_filename


def generate_smooth_data():
    directory = "../../DATA/1_interpolated/"
    for file in os.listdir(directory):
        for i in [3, 5, 7, 9, 11, 13, 15]:
            smoothed_dataset = smooth_data_utils.generate_smooth_dataframe(file, directory, "savgol", window=i)
            new_filename = f"./wind_{i}/" + file.replace("interpolated", "smoothed")
            smoothed_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')


def show_histograms_with_vmax():
    fig, axs = plt.subplots(2, 4)

    directory = "../../DATA/1_interpolated/"
    v_max_list = {}
    for file in os.listdir(directory):
        v_vector = calculate_velocity_vector_for_dataset_filename(file, directory)
        v_trajectory = sqrt(v_vector[:, 0] ** 2 + v_vector[:, 1] ** 2 + v_vector[:, 2] ** 2)
        v_max = max(v_trajectory)
        if v_max > 800:
            print(f"v_max is {v_max} in file {file}")
        else:
            v_max_list.update({file: v_max})
    axs[0, 0].hist(v_max_list.values())
    axs[0, 0].set_title(f"raw")

    for i in [3, 5, 7, 9, 11, 13, 15]:
        directory = f"./wind_{i}/"
        v_max_list = {}
        for file in os.listdir(directory):
            v_vector = calculate_velocity_vector_for_dataset_filename(file, directory)
            v_trajectory = sqrt(v_vector[:, 0] ** 2 + v_vector[:, 1] ** 2 + v_vector[:, 2] ** 2)
            v_max = max(v_trajectory)
            if v_max > 100:
                pass
                # print(f"v_max is {v_max} in file {file}")
            else:
                v_max_list.update({file: v_max})
        if i == 3:
            axs[0, 1].hist(v_max_list.values())
            axs[0, 1].set_title(f"window = {i}")
        elif i == 5:
            axs[0, 2].hist(v_max_list.values())
            axs[0, 2].set_title(f"window = {i}")
        elif i == 7:
            axs[0, 3].hist(v_max_list.values())
            axs[0, 3].set_title(f"window = {i}")
        elif i == 9:
            axs[1, 0].hist(v_max_list.values())
            axs[1, 0].set_title(f"window = {i}")
        elif i == 11:
            axs[1, 1].hist(v_max_list.values())
            axs[1, 1].set_title(f"window = {i}")
        elif i == 13:
            axs[1, 2].hist(v_max_list.values())
            axs[1, 2].set_title(f"window = {i}")
        elif i == 15:
            axs[1, 3].hist(v_max_list.values())
            axs[1, 3].set_title(f"window = {i}")
    plt.show()


def show_examples_of_velocities(file="rand"):
    dir_int = "../../DATA/1_interpolated/"
    if file == "rand":
        files = os.listdir(dir_int)
        shuffle(files)
        file = files[0]
    v_vector = calculate_velocity_vector_for_dataset_filename(file, dir_int)
    v_trajectory = sqrt(v_vector[:, 0] ** 2 + v_vector[:, 1] ** 2 + v_vector[:, 2] ** 2)
    plt.plot(v_trajectory, label=f"raw")
    plt.title(file)
    file = file.replace("interpolated", "smoothed")
    for i in [3, 5, 7, 9, 11, 13, 15]:
        dir_smooth = f"./wind_{i}/"
        v_vector = calculate_velocity_vector_for_dataset_filename(file, dir_smooth)
        v_trajectory = sqrt(v_vector[:, 0] ** 2 + v_vector[:, 1] ** 2 + v_vector[:, 2] ** 2)
        plt.plot(v_trajectory, label=f"window={i}")
    print(file)
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    generate_smooth_data()
    # show_histograms_with_vmax()
    # show_examples_of_velocities("20200423134_interpolated_L.csv")
    show_examples_of_velocities("20200423307_interpolated_R.csv")
