import math

from numpy import median
import numpy as np
import pandas as pd
from numpy import mean, median
from scipy.signal import savgol_filter

from ArmMovementPredictionStudien.PREPROCESSING.utils import velocity
from ArmMovementPredictionStudien.PREPROCESSING.utils.utils import open_dataset_numpy


def filter_dataset(filename, directory, method, window=7):
    dataset = open_dataset_numpy(filename, directory)
    if method == "median":
        return median_filter(dataset, window)
    elif method == "mean":
        return mean_filter(dataset, window)
    elif method == "sma":
        return sma_filter(dataset, window)
    elif method == "dynamic":
        return dynamic_filter(dataset, window)
    elif method == "savgol":
        return savitzky_golay(dataset, window)
    else:
        raise Exception("Choose a filter method: 'median', 'mean', 'sma', 'savgol'")


def generate_smooth_dataframe(filename, directory, method, window=7):
    """
    Generates a smoothed Pandas Dataframe from a dataset by its filename.
    This smooths only the position data, not the velocity!

    :param filename: Filename of position-data
    :param directory: Directory of position-data
    :param window: 3 uses the adjacent values of every value in the dataset, 5 the next two adjacent values
     7 the next three values
    :return: returns a dataframe of smoothed position-data
    """
    dataset_smooth = filter_dataset(filename, directory, method, window)
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


def mean_filter(dataset, window=7):
    return window_before_and_after(dataset, "mean", window=window)


def median_filter(dataset, window=7):
    return window_before_and_after(dataset, "median", window=window)


def sma_filter(dataset, window):
    return window_before(dataset, window=window)


def dynamic_filter(dataset, window):
    return window_dynamic(dataset, window=window)


def window_before_and_after(dataset, method, window=7):
    last_index = len(dataset) - 1
    filtered_dataset = np.empty(shape=(len(dataset), 9))

    if window == 3:
        filtered_dataset[0] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(1, len(dataset) - 1):
            values = [dataset[i - 1],
                      dataset[i],
                      dataset[i + 1]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 5:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(2, len(dataset) - 2):
            values = [dataset[i - 2], dataset[i - 1],
                      dataset[i],
                      dataset[i + 1], dataset[i + 2]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 7:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[2] = float('nan')
        filtered_dataset[last_index - 2] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(3, len(dataset) - 3):
            values = [dataset[i - 3], dataset[i - 2], dataset[i - 1],
                      dataset[i],
                      dataset[i + 1], dataset[i + 2], dataset[i + 3]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 9:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[2] = float('nan')
        filtered_dataset[3] = float('nan')
        filtered_dataset[last_index - 3] = float('nan')
        filtered_dataset[last_index - 2] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(4, len(dataset) - 4):
            values = [dataset[i - 4], dataset[i - 3], dataset[i - 2], dataset[i - 1],
                      dataset[i],
                      dataset[i + 1], dataset[i + 2], dataset[i + 3], dataset[i + 4]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 11:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[2] = float('nan')
        filtered_dataset[3] = float('nan')
        filtered_dataset[4] = float('nan')
        filtered_dataset[last_index - 4] = float('nan')
        filtered_dataset[last_index - 3] = float('nan')
        filtered_dataset[last_index - 2] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(5, len(dataset) - 5):
            values = [dataset[i - 5], dataset[i - 4], dataset[i - 3], dataset[i - 2], dataset[i - 1],
                      dataset[i],
                      dataset[i + 1], dataset[i + 2], dataset[i + 3], dataset[i + 4], dataset[i + 5]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 13:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[2] = float('nan')
        filtered_dataset[3] = float('nan')
        filtered_dataset[4] = float('nan')
        filtered_dataset[5] = float('nan')
        filtered_dataset[last_index - 5] = float('nan')
        filtered_dataset[last_index - 4] = float('nan')
        filtered_dataset[last_index - 3] = float('nan')
        filtered_dataset[last_index - 2] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(6, len(dataset) - 6):
            values = [dataset[i - 6], dataset[i - 5], dataset[i - 4], dataset[i - 3], dataset[i - 2], dataset[i - 1],
                      dataset[i],
                      dataset[i + 1], dataset[i + 2], dataset[i + 3], dataset[i + 4], dataset[i + 5], dataset[i + 6]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    elif window == 15:
        filtered_dataset[0] = float('nan')
        filtered_dataset[1] = float('nan')
        filtered_dataset[2] = float('nan')
        filtered_dataset[3] = float('nan')
        filtered_dataset[4] = float('nan')
        filtered_dataset[5] = float('nan')
        filtered_dataset[6] = float('nan')
        filtered_dataset[last_index - 6] = float('nan')
        filtered_dataset[last_index - 5] = float('nan')
        filtered_dataset[last_index - 4] = float('nan')
        filtered_dataset[last_index - 3] = float('nan')
        filtered_dataset[last_index - 2] = float('nan')
        filtered_dataset[last_index - 1] = float('nan')
        filtered_dataset[last_index] = float('nan')

        for i in range(7, len(dataset) - 7):
            values = [dataset[i - 7], dataset[i - 6], dataset[i - 5], dataset[i - 4], dataset[i - 3], dataset[i - 2],
                      dataset[i - 1],
                      dataset[i],
                      dataset[i + 1],
                      dataset[i + 2], dataset[i + 3], dataset[i + 4], dataset[i + 5], dataset[i + 6], dataset[i + 7]]
            if method == "median":
                average = median(values, axis=0)
            elif method == "mean":
                average = mean(values, axis=0)
            else:
                average = 0
            filtered_dataset[i] = average

    else:
        raise Exception("Window has to be 3; 5; 7; 9; 11; 13 or 15")
    return filtered_dataset


def window_before(dataset, window=7):
    filtered_dataset = np.empty(shape=(len(dataset), 9))

    if len(dataset) <= window:
        raise Exception(f"Dataset is to short: {len(dataset)} entries.")

    if 0 <= window < 16:
        for i in range(0, window):
            filtered_dataset[i] = dataset[i]

        for i in range(window, len(dataset)):
            values = [dataset[i]]
            for j in range(0, window):
                values.append(dataset[i - j - 1])
            average = mean(values, axis=0)
            filtered_dataset[i] = average
    else:
        raise Exception("Window has to be in [0; 15]")

    return filtered_dataset


def window_dynamic(dataset, window=7):
    print("DO NOT USE THIS FILTER, SOME VALUES ARE BEING CALCULATED TWICE BECAUSE OF THE DYNAMIC WINDOW")
    filtered_dataset = np.empty(shape=(len(dataset), 9))

    if len(dataset) <= window:
        raise Exception(f"Dataset is to short: {len(dataset)} entries.")

    if 0 < window > 16:
        raise Exception("Window has to be in [0; 15]")

    for index in range(0, len(dataset)):
        p_rel = math.ceil((index * window) / len(dataset))
        if p_rel < 0.1:
            p_rel = 1
        if p_rel > window:
            p_rel = window
        lower_bound = p_rel - 1
        upper_bound = window - p_rel

        values = []
        for j in range(index - lower_bound, index + upper_bound + 1):
            values.append(dataset[j])
        average = mean(values, axis=0)
        filtered_dataset[index] = average

    return filtered_dataset


def savitzky_golay(dataset, window):
    if window == 3 or 5:
        order = 1
    elif window == 7 or 9:
        order = 2
    elif window == 11 or 13:
        order = 3
    else:
        order = 4
    return savgol_filter(dataset, window, order, axis=0)
