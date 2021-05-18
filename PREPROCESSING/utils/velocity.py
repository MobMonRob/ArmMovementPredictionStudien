import os

from numpy import gradient, sqrt
import pandas as pd
from outliers import smirnov_grubbs as grubbs

from ArmMovementPredictionStudien.PREPROCESSING.utils.utils import open_dataset_numpy


def determine_left_or_right_dataset(filename):
    if '_R' in filename:
        return "R"
    if '_L' in filename:
        return "L"
    return "X"


def calculate_velocity_vector_for_dataset_filename(filename, directory, remove_outliers=True):
    dataset = open_dataset_numpy(filename, directory)
    dataset_velocity = \
        calculate_velocity_vector_for_dataset(dataset, remove_outliers=remove_outliers, filename=filename)
    return dataset_velocity


def calculate_velocity_vector_for_dataset(dataset, remove_outliers=True, filename='dataset'):
    dataset_velocity = gradient(dataset, axis=0)
    if len(dataset_velocity) < 5:
        print(f"{filename} has length {len(dataset_velocity)}")
    elif remove_outliers:
        try:
            for col in range(0, len(dataset_velocity[0]) - 1):
                indices = grubbs.two_sided_test_indices(dataset_velocity[:, col], alpha=0.01)  # alpha needs to be so small
                for i in indices:
                    dataset_velocity[i, col] = float('NaN')
        except TypeError:
            print(f"No len() in {filename}")
    return dataset_velocity


def calculate_velocity_of_trajectory(dataset, joint_type="w"):
    if joint_type == "w":
        return sqrt(dataset.iloc[:, 0] ** 2 + dataset.iloc[:, 1] ** 2 + dataset.iloc[:, 2] ** 2)
    if joint_type == "e":
        return sqrt(dataset.iloc[:, 3] ** 2 + dataset.iloc[:, 4] ** 2 + dataset.iloc[:, 5] ** 2)
    if joint_type == "gh":
        return sqrt(dataset.iloc[:, 6] ** 2 + dataset.iloc[:, 7] ** 2 + dataset.iloc[:, 8] ** 2)
    raise Exception("Choose 'w' for wrist, 'e' for elbow or 'gh' for shoulder")


def generate_velocity_dataframe(filename, directory, remove_outliers=True):
    dataset_velocity = calculate_velocity_vector_for_dataset_filename(filename, directory, remove_outliers)
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


def generate_acceleration_dataframe(dataset, filename='dataset', remove_outliers=True):
    dataset_velocity = \
        calculate_velocity_vector_for_dataset(dataset, filename=filename, remove_outliers=remove_outliers)
    dataset_acceleration = \
        calculate_velocity_vector_for_dataset(dataset_velocity, filename=filename, remove_outliers=remove_outliers)
    right_or_left = determine_left_or_right_dataset(filename)
    column_names = [
        "a_{r_l}WJC_x".format(r_l=right_or_left),
        "a_{r_l}WJC_y".format(r_l=right_or_left),
        "a_{r_l}WJC_z".format(r_l=right_or_left),
        "a_{r_l}EJC_x".format(r_l=right_or_left),
        "a_{r_l}EJC_y".format(r_l=right_or_left),
        "a_{r_l}EJC_z".format(r_l=right_or_left),
        "a_{r_l}GHJC_x".format(r_l=right_or_left),
        "a_{r_l}GHJC_y".format(r_l=right_or_left),
        "a_{r_l}GHJC_z".format(r_l=right_or_left)
    ]
    dataframe_acceleration = pd.DataFrame(
        data=dataset_acceleration,
        columns=[column_names]
    )
    return dataframe_acceleration


def write_velocity_dataset_to_csv(filename, directory):
    dataframe_velocity = generate_velocity_dataframe(filename, directory)
    new_filename = "../../DATA/data_velocity/" + filename.replace("truncated", "velocity")
    dataframe_velocity.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
