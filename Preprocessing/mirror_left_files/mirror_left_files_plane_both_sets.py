import os
from math import sqrt
from shutil import copy

import pandas as pd
import numpy as np
from numpy.linalg import norm

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas


def get_p1(dataset_l, dataset_r):
    for index, row in dataset_l.iterrows():
        if index in dataset_r.index:
            if not row[0:3].isnull().values.any() and not dataset_r.iloc[index, 0:3].isnull().values.any():
                p1_l = dataset_l.iloc[index, 0:3]
                p1_r = dataset_r.iloc[index, 0:3]
                return (np.array(p1_l) + np.array(p1_r)) / 2


def get_p2(dataset_l, dataset_r):
    for index, row in dataset_l[::-1].iterrows():
        if index in dataset_r.index:
            if not row[0:3].isnull().values.any() and not dataset_r.iloc[index, 0:3].isnull().values.any():
                p2_l = dataset_l.iloc[index, 0:3]
                p2_r = dataset_r.iloc[index, 0:3]
                return (np.array(p2_l) + np.array(p2_r)) / 2


def get_p1_p2(dataset_l, dataset_r):
    return get_p1(dataset_l, dataset_r), get_p2(dataset_l, dataset_r)


def get_farest_distant_point(dataset_l, p1, p2):
    max_d = 0
    max_ind = 0
    for index, row in dataset_l.iterrows():
        p3 = row.iloc[0:3]
        d = norm(np.cross(p2 - p1, p1 - p3)) / norm(p2 - p1)
        if d > max_d:
            max_d = d
            max_ind = index
    return max_ind, max_d


def get_normed_vector(dataset_l, dataset_r):
    p1, p2 = get_p1_p2(dataset_l, dataset_r)

    max_ind, max_d = get_farest_distant_point(dataset_l, p1, p2)
    p3 = dataset_l.iloc[max_ind, 0:3]

    p1p2_normalized = (p2 - p1) / norm(p2 - p1)
    d_p3p1 = norm(p3 - p1)
    p1m = sqrt(d_p3p1 ** 2 - max_d ** 2)
    m = p1 + p1m * p1p2_normalized
    p3m_normalized = (p3 - m) / norm(p3 - m)
    return m, p3m_normalized


def get_a_b_c_d(dataset_l, dataset_r):
    p, n = get_normed_vector(dataset_l, dataset_r)
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


def mirror_file_both_sets(dataset_l, dataset_r):
    a, b, c, d = get_a_b_c_d(dataset_l, dataset_r)
    dataset_left = pd.DataFrame(columns=dataset_l.columns)

    for index, row in dataset_l.iterrows():
        x = row[0]
        y = row[1]
        z = row[2]
        mirrored_w = calculate_coordinates_of_mirrored_point(a, b, c, d, x, y, z)
        dataset_left.loc[index, 0:3] = mirrored_w
        dataset_left.loc[index, 3:6] = dataset_l.iloc[index, 3:6]
        dataset_left.loc[index, 6:9] = dataset_l.iloc[index, 6:9]
    return dataset_left
