import os
from math import sqrt
from shutil import copy

import pandas as pd
import numpy as np
from numpy.linalg import norm

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas


def calculate_coordinates_of_mirrored_point(line_startpoint, line_endpoint, point_to_mirror):
    p1 = line_startpoint
    p2 = line_endpoint
    p3 = point_to_mirror

    p1p2_normalized = (p2 - p1) / norm(p2 - p1)
    d_p3p1 = norm(p3 - p1)
    d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)  # area of parallelogram divided by one side equals height

    p1m = sqrt(d_p3p1 ** 2 - d ** 2)
    m = p1 + p1m * p1p2_normalized

    p3_1 = m + (m - p3)
    return p3_1


directory = "../../DATA/3_truncated/"
filelist_left = []

for file in os.listdir(directory):
    if "_L" in file:
        filelist_left.append(file)
    if "_R" in file:
        filename = file.replace("truncated", "mirrored")
        copy(directory + file, "../../DATA/4_mirrored/" + filename)

for file in filelist_left:
    dataset = open_dataset_pandas(file, directory=directory)
    startpoint_w = dataset.iloc[0, 0:3]
    endpoint_w = dataset.iloc[-1, 0:3]
    startpoint_e = dataset.iloc[0, 3:6]
    endpoint_e = dataset.iloc[-1, 3:6]
    startpoint_gh = dataset.iloc[0, 6:9]
    endpoint_gh = dataset.iloc[-1, 6:9]
    dataset_left = pd.DataFrame(columns=dataset.columns)

    dataset_left.loc[0, 0:3] = startpoint_w
    dataset_left.loc[0, 3:6] = startpoint_e
    dataset_left.loc[0, 6:9] = startpoint_gh
    for index, row in dataset.iterrows():
        if 0 < index < dataset.index[-1]:
            mirrored_w = calculate_coordinates_of_mirrored_point(startpoint_w, endpoint_w, row.iloc[0:3])
            mirrored_e = calculate_coordinates_of_mirrored_point(startpoint_e, endpoint_e, row.iloc[3:6])
            mirrored_gh = calculate_coordinates_of_mirrored_point(startpoint_gh, endpoint_gh, row.iloc[6:9])
            dataset_left.loc[index, 0:3] = mirrored_w
            dataset_left.loc[index, 3:6] = mirrored_e
            dataset_left.loc[index, 6:9] = mirrored_gh
    dataset_left.loc[dataset.index[-1], 0:3] = endpoint_w
    dataset_left.loc[dataset.index[-1], 3:6] = endpoint_e
    dataset_left.loc[dataset.index[-1], 6:9] = endpoint_gh

    new_filename = "../../DATA/4_mirrored/" + file.replace("truncated", "mirrored")
    dataset_left.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')


