import os

from numpy import gradient
import pandas as pd
from outliers import smirnov_grubbs as grubbs

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_numpy


def determine_left_or_right_dataset(filename):
    if '_R' in filename:
        return "R"
    if '_L' in filename:
        return "L"
    return "X"


def calculate_velocity_vector_for_dataset(filename, directory, remove_outliers=True):
    dataset = open_dataset_numpy(filename, directory)
    dataset_velocity = gradient(dataset, axis=0)
    if remove_outliers:
        for col in range(0, len(dataset_velocity[0]) - 1):
            indices = grubbs.two_sided_test_indices(dataset_velocity[:, col], alpha=0.01)  # alpha needs to be so small
            for i in indices:
                dataset_velocity[i, col] = float('NaN')
    return dataset_velocity


def generate_velocity_dataframe(filename, directory):
    dataset_velocity = calculate_velocity_vector_for_dataset(filename, directory)
    right_or_left = determine_left_or_right_dataset(filename)
    column_names = [
        "v_{r_l}WJC_x".format(r_l=right_or_left),
        "v_{r_l}WJC_y".format(r_l=right_or_left),
        "v_{r_l}WJC_z".format(r_l=right_or_left),
        "v_{r_l}EJC_x".format(r_l=right_or_left),
        "v_{r_l}EJC_y".format(r_l=right_or_left),
        "v_{r_l}EJC_z".format(r_l=right_or_left),
        "v_{r_l}GHJC_x".format(r_l=right_or_left),
        "v_{r_l}GHJC_y".format(r_l=right_or_left),
        "v_{r_l}GHJC_z".format(r_l=right_or_left)
    ]
    dataframe_velocity = pd.DataFrame(
        data=dataset_velocity,
        columns=[column_names]
    )
    return dataframe_velocity


def write_velocity_dataset_to_csv(filename, directory):
    dataframe_velocity = generate_velocity_dataframe(filename, directory)
    new_filename = "../../DATA/data_velocity/" + filename.replace("truncated", "velocity")
    dataframe_velocity.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')


if __name__ == '__main__':
    temp_directory = "../../DATA/3_truncated/"
    for file in os.listdir(temp_directory):
        write_velocity_dataset_to_csv(file, temp_directory)
