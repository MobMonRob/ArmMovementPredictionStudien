from numpy import sqrt
import pandas as pd

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
from ArmMovementPredictionStudien.Preprocessing.utils.velocity import generate_velocity_dataframe


def find_maximum_velocity_of_trajectory(dataset, joint_type="w"):
    velocity_data = calculate_velocity_of_trajectory(dataset, joint_type)
    max_v_index = velocity_data.abs().idxmax()
    v_max = abs(velocity_data[max_v_index])
    return pd.DataFrame(data={"index_v_max": [max_v_index], "v_max": [v_max]})


def find_maximum_velocity_of_single_dimension(dataset: pd.DataFrame, dimension="x", joint_type="w"):
    column = determine_index_of_column(dimension, joint_type)
    velocity_data = dataset.iloc[:, column]
    max_v_index = velocity_data.abs().idxmax()
    v_max = abs(velocity_data[max_v_index])
    return pd.DataFrame(data={"index_v_max": [max_v_index], "v_max": [v_max]})


def calculate_velocity_of_trajectory(dataset, joint_type="w"):
    if joint_type == "w":
        return sqrt(dataset.iloc[:, 0] ** 2 + dataset.iloc[:, 1] ** 2 + dataset.iloc[:, 2] ** 2)
    if joint_type == "e":
        return sqrt(dataset.iloc[:, 3] ** 2 + dataset.iloc[:, 4] ** 2 + dataset.iloc[:, 5] ** 2)
    if joint_type == "gh":
        return sqrt(dataset.iloc[:, 6] ** 2 + dataset.iloc[:, 7] ** 2 + dataset.iloc[:, 8] ** 2)
    raise Exception("Choose 'w' for wrist, 'e' for elbow or 'gh' for shoulder")


def round_velocity_below_threshold_to_zero(dataset: pd.DataFrame, joint_type="w", threshold=0.01):
    threshold_dataset = dataset.copy()
    for dimension in ['x', 'y', 'z']:
        v_max = \
            find_maximum_velocity_of_single_dimension(dataset, dimension=dimension, joint_type=joint_type)[
                "v_max"].values[0]
        v_threshold = v_max * threshold
        column = determine_index_of_column(dimension, joint_type)
        threshold_dataset.iloc[:, column] = threshold_dataset.iloc[:, column].apply(round_values, args=(v_threshold, 0))
    return threshold_dataset


def round_values(value, v_threshold, _):
    if abs(value) < v_threshold:
        return 0
    else:
        return value


def find_nearest_minima_from_maximum(dataset, joint_type="w", threshold=0.01):
    """
    Finds next index from maximum velocity to the left and to the right where value is zero.
        index_left and index_right are the most outer indexes still contained in the dataset.

    :param dataset:
    :param joint_type:
    :param threshold:
    :return:
    """
    threshold_dataset = round_velocity_below_threshold_to_zero(dataset, joint_type=joint_type, threshold=threshold)
    threshold_trajectory_dataset = calculate_velocity_of_trajectory(threshold_dataset, joint_type)
    index_v_max = \
        find_maximum_velocity_of_trajectory(dataset, joint_type=joint_type)["index_v_max"].values[0]
    max_index = len(threshold_trajectory_dataset) - 1
    index_left = 0
    index_right = max_index

    for index in range(index_v_max, -1, -1):
        if abs(threshold_trajectory_dataset[index]) < 0.0001:
            index_left = index + 1
            break
    for index in range(index_v_max, max_index + 1):
        if abs(threshold_trajectory_dataset[index]) < 0.0001:
            index_right = index - 1
            break
    return [index_left, index_right]


def find_nearest_minimum_from_maximum_left_per_dimension(dataset, joint_type="w"):
    index_left = pd.DataFrame({'x': [0], 'y': [0], 'z': [0]})
    for dimension in ['x', 'y', 'z']:
        index_v_max = \
            find_maximum_velocity_of_single_dimension(dataset, dimension=dimension, joint_type=joint_type)[
                "index_v_max"].values[0]
        column = determine_index_of_column(dimension, joint_type)
        for index in range(index_v_max, -1, -1):
            if dataset.iloc[index, column] < 0.0001:
                index_left[dimension] = index + 1
                break
    return index_left


def find_nearest_minimum_from_maximum_right_per_dimension(dataset, joint_type="w"):
    max_index = len(dataset) - 1
    index_right = pd.DataFrame({'x': [max_index], 'y': [max_index], 'z': [max_index]})
    for dimension in ['x', 'y', 'z']:
        index_v_max = \
            find_maximum_velocity_of_single_dimension(dataset, dimension=dimension, joint_type=joint_type)[
                "index_v_max"].values[0]
        column = determine_index_of_column(dimension, joint_type)
        for index in range(index_v_max, max_index + 1):
            if dataset.iloc[index, column] < 0.0001:
                index_right[dimension] = index - 1
                break
    return index_right


def truncate_dataset_velocity(dataset: pd.DataFrame, joint_type="w", threshold=0.01):
    """
    Truncates **velocity** dataset from last zero value before maximum velocity to following zero value.

    :param dataset: Input velocity dataset
    :param joint_type: Chooses which joint type is used to truncate the whole dataset (w, e, gh)
    :param threshold: factor for maximum velocity, every value below threshold*v_max is set to zero.
        Threshold=0 uses original dataset.
    :return: new truncated dataset, indexes stay the same
    """
    [index_left, index_right] = find_nearest_minima_from_maximum(dataset, joint_type=joint_type, threshold=threshold)
    truncated_dataset = dataset.truncate(before=index_left, after=index_right)
    return truncated_dataset


def truncate_dataset_position(filename, joint_type="w", threshold=0.01, directory="./2_smoothed/"):
    """
    Truncates dataset **with raw position data** from last zero value before maximum velocity to following zero value.

    :param filename: Input filename of position dataset
    :param joint_type: Chooses which joint type is used to truncate the whole dataset (w, e, gh)
    :param threshold: factor for maximum velocity, every value below threshold*v_max is set to zero.
        Threshold=0 uses original dataset.
    :param directory: directory of files
    :return: new truncated dataset as dataframe, indexes stay the same
    """

    dataset = open_dataset_pandas(filename, directory=directory)
    dataset_velocity = generate_velocity_dataframe(filename, directory)
    [index_left, index_right] = \
        find_nearest_minima_from_maximum(dataset_velocity, joint_type=joint_type, threshold=threshold)
    truncated_dataset = dataset.truncate(before=index_left, after=index_right)
    return truncated_dataset


def determine_index_of_column(dimension, joint_type):
    if dimension == "x":
        column = 0
    elif dimension == "y":
        column = 1
    elif dimension == "z":
        column = 2
    else:
        raise Exception("Input values for dimension have to be 'x', 'y' or 'z'.")

    if joint_type == "w":
        column += 0
    elif joint_type == "e":
        column += 1
    elif joint_type == "gh":
        column += 2
    else:
        raise Exception("Choose 'w' for wrist, 'e' for elbow or 'gh' for shoulder")
    return column
