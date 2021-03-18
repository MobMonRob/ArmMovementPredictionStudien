from numpy import median
import numpy as np
import pandas as pd

from ArmMovementPredictionStudien.Preprocessing.utils import velocity
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_numpy


def filter_dataset(filename, directory, window=5):
    dataset = open_dataset_numpy(filename, directory)
    return median_filter(dataset, window)


def generate_smooth_dataframe(filename, directory, window=5):
    """
    Generates a smoothed Pandas Dataframe from a dataset by its filename.
    This smooths only the position data, not the velocity!

    :param filename: Filename of position-data
    :param directory: Directory of position-data
    :param window: 3 uses the adjacent values of every value in the dataset, 5 the next two adjacent values
     7 the next three values
    :return: returns a dataframe of smoothed position-data
    """
    dataset_smooth = filter_dataset(filename, directory, window)
    right_or_left = velocity.determine_left_or_right_dataset(filename)
    column_names = [
        "{r_l}WJC_x".format(r_l=right_or_left),
        "{r_l}WJC_y".format(r_l=right_or_left),
        "{r_l}WJC_z".format(r_l=right_or_left),
        "{r_l}EJC_x".format(r_l=right_or_left),
        "{r_l}EJC_y".format(r_l=right_or_left),
        "{r_l}EJC_z".format(r_l=right_or_left),
        "{r_l}GHJC_x".format(r_l=right_or_left),
        "{r_l}GHJC_y".format(r_l=right_or_left),
        "{r_l}GHJC_z".format(r_l=right_or_left)
    ]
    dataframe_smooth = pd.DataFrame(
        data=dataset_smooth,
        columns=[column_names]
    )
    return dataframe_smooth


def median_filter(dataset, window=5):
    last_index = len(dataset) - 1
    filtered_dataset = np.empty(shape=(len(dataset), 9))
    count = 0
    if window == 3:
        filtered_dataset[0] = np.empty(9)
        filtered_dataset[last_index] = np.empty(9)

        for i in range(1, len(dataset) - 1):
            values = [dataset[i - 1], dataset[i],
                      dataset[i + 1]]
            median_number = median(values, axis=0)
            filtered_dataset[count] = median_number
            count += 1

    elif window == 5:
        filtered_dataset[0] = np.empty(9)
        filtered_dataset[1] = np.empty(9)
        filtered_dataset[last_index - 1] = np.empty(9)
        filtered_dataset[last_index] = np.empty(9)

        for i in range(2, len(dataset) - 2):
            values = [dataset[i - 2], dataset[i - 1], dataset[i],
                      dataset[i + 1], dataset[i + 2]]
            median_number = median(values, axis=0)
            filtered_dataset[count] = median_number
            count += 1

    elif window == 7:
        filtered_dataset[0] = np.empty(9)
        filtered_dataset[1] = np.empty(9)
        filtered_dataset[2] = np.empty(9)
        filtered_dataset[last_index - 2] = np.empty(9)
        filtered_dataset[last_index - 1] = np.empty(9)
        filtered_dataset[last_index] = np.empty(9)

        for i in range(3, len(dataset) - 3):
            values = [dataset[i - 3], dataset[i - 2], dataset[i - 1], dataset[i],
                      dataset[i + 1], dataset[i + 2], dataset[i + 3]]
            median_number = median(values, axis=0)
            filtered_dataset[count] = median_number
            count += 1

    else:
        raise Exception("Window has to be 3 or 5 or 7")
    return filtered_dataset
