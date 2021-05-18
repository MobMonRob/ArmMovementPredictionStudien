import os
from math import sqrt
from shutil import copy

import pandas as pd
import numpy as np
from numpy.linalg import norm

from ArmMovementPredictionStudien.PREPROCESSING.utils.utils import open_dataset_pandas


def get_farest_distant_point(dataset):
    p1 = dataset.iloc[0, 0:3]
    p2 = dataset.iloc[-1, 0:3]
    max_d = 0
    max_ind = 0
    for index, row in dataset.iterrows():
        p3 = row.iloc[0:3]
        d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
        if d > max_d:
            max_d = d
            max_ind = index
    return max_ind, max_d


def get_normed_vector(dataset):
    p1 = dataset.iloc[0, 0:3]
    p2 = dataset.iloc[-1, 0:3]

    max_ind, max_d = get_farest_distant_point(dataset)
    p3 = dataset.iloc[max_ind, 0:3]

    p1p2_normalized = (p2 - p1) / norm(p2 - p1)
    d_p3p1 = norm(p3 - p1)
    p1m = sqrt(d_p3p1 ** 2 - max_d ** 2)
    m = p1 + p1m * p1p2_normalized
    p3m_normalized = (p3 - m) / norm(p3 - m)
    return m, p3m_normalized


def get_a_b_c_d(dataset):
    p, n = get_normed_vector(dataset)
    d = -np.dot(p, n)
    return n[0], n[1], n[2], d


def calculate_coordinates_of_mirrored_point(a, b, c, d, x1, y1, z1):
    k = (-a * x1 - b * y1 - c * z1 - d) / float((a * a + b * b + c * c))
    x2 = a * k + x1
    y2 = b * k + y1
    z2 = c * k + z1
    x3 = 2 * x2 - x1
    y3 = 2 * y2 - y1
    z3 = 2 * z2 - z1
    return np.array([x3, y3, z3])


def mirror_file_one_set(dataset):
    a, b, c, d = get_a_b_c_d(dataset)
    dataset_left = pd.DataFrame(columns=dataset.columns)

    dataset_left.at[0, 0:3] = dataset.iloc[0, 0:3]
    dataset_left.at[0, 3:6] = dataset.iloc[0, 3:6]
    dataset_left.at[0, 6:9] = dataset.iloc[0, 6:9]
    for index, row in dataset.iterrows():
        if 0 < index < dataset.index[-1]:
            mirrored_w = calculate_coordinates_of_mirrored_point(a, b, c, d, row[0], row[1], row[2])
            mirrored_e = calculate_coordinates_of_mirrored_point(a, b, c, d, row[3], row[4], row[5])
            mirrored_s = calculate_coordinates_of_mirrored_point(a, b, c, d, row[6], row[7], row[8])
            dataset_left.at[index, 0:3] = mirrored_w
            dataset_left.at[index, 3:6] = mirrored_e
            dataset_left.at[index, 6:9] = mirrored_s
    dataset_left.at[dataset.index[-1], 0:3] = dataset.iloc[dataset.index[-1], 0:3]
    dataset_left.at[dataset.index[-1], 3:6] = dataset.iloc[dataset.index[-1], 3:6]
    dataset_left.at[dataset.index[-1], 6:9] = dataset.iloc[dataset.index[-1], 6:9]

    return dataset_left
