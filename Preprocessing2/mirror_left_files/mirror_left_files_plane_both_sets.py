import os
from math import sqrt
from shutil import copy

import pandas as pd
import numpy as np
from numpy.linalg import norm


# def get_p1(dataset_l, dataset_r):
#     for index, row in dataset_l.iterrows():
#         if index in dataset_r.index:
#             if not row[0:3].isnull().values.any() and not dataset_r.iloc[index, 0:3].isnull().values.any():
#                   TODO: testen: sollte nur einmal durchlaufen
#                 p1_l = dataset_l.iloc[index, 0:3]
#                 p1_r = dataset_r.iloc[index, 0:3]
#                 return (np.array(p1_l) + np.array(p1_r)) / 2
#
#
# def get_p2(dataset_l, dataset_r):
#     for index, row in dataset_l[::-1].iterrows():
#         if index in dataset_r.index:
#             if not row[0:3].isnull().values.any() and not dataset_r.iloc[index, 0:3].isnull().values.any():
#                 p2_l = dataset_l.iloc[index, 0:3]
#                 p2_r = dataset_r.iloc[index, 0:3]
#                 return (np.array(p2_l) + np.array(p2_r)) / 2
#
#
# def get_p1_p2(dataset_l, dataset_r):
#     return get_p1(dataset_l, dataset_r), get_p2(dataset_l, dataset_r)
#
#
# def get_normed_vector(dataset_l, dataset_r):
#     p1, p2 = get_p1_p2(dataset_l, dataset_r)
#
#     max_ind, max_d = get_farest_distant_point(dataset_l, p1, p2)
#     p3 = dataset_l.iloc[max_ind, 0:3]
#
#     p1p2_normalized = (p2 - p1) / norm(p2 - p1)
#     d_p3p1 = norm(p3 - p1)
#     p1m = sqrt(d_p3p1 ** 2 - max_d ** 2)
#     m = p1 + p1m * p1p2_normalized
#     p3m_normalized = (p3 - m) / norm(p3 - m)
#     return m, p3m_normalized


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


def get_p1_p2(dataset_l, dataset_r):
    p1l = dataset_l.iloc[0, 0:3]
    p1r = dataset_r.iloc[0, 0:3]
    p1 = (p1l + p1r.values) / 2
    p2l = dataset_l.iloc[-1, 0:3]
    p2r = dataset_r.iloc[-1, 0:3]
    p2 = (p2l + p2r.values) / 2
    return p1, p2


def get_normed_vector(dataset_l, dataset_r):
    p1, p2 = get_p1_p2(dataset_l, dataset_r)
    p1p2_normalized = (p2 - p1) / norm(p2 - p1)

    # calculate normed vector p1l - p1m
    p1l = dataset_l.iloc[0, 0:3]
    d_p1lp1m = norm(np.cross(p1l - p1, p2 - p1)) / norm(p2 - p1)  # distance p1l to p1m
    d_p1lp1 = norm(p1l - p1)
    p1p1m = sqrt(abs(d_p1lp1 ** 2 - d_p1lp1m ** 2))
    p1m = p1 + p1p1m * p1p2_normalized
    p1lp1m_norm = (p1m - p1l) / norm(p1m - p1l)

    # calculate normed vector p2l - p2m
    p2l = dataset_l.iloc[-1, 0:3]
    d_p2lp2m = norm(np.cross(p2l - p2, p2 - p1)) / norm(p2 - p1)  # distance p2l to p2m
    d_p2lp2 = norm(p2l - p2)
    p2p2m = sqrt(abs(d_p2lp2 ** 2 - d_p2lp2m ** 2))
    p2m = p2 + p2p2m * p1p2_normalized
    p2lp2m_norm = (p2m - p2l) / norm(p2m - p2l)

    # calculate normed vector of farest away point
    max_ind, d_p3lp3m = get_farest_distant_point(dataset_l, p1, p2)
    p3l = dataset_l.iloc[max_ind, 0:3]
    d_p3lp1 = norm(p3l - p1)
    p3lp1 = sqrt(abs(d_p3lp1 ** 2 - d_p3lp3m ** 2))
    p3m = p1 + p3lp1 * p1p2_normalized
    p3lp3m_norm = (p3m - p3l) / norm(p3m - p3l)

    # take average of both start and endpoint normed vector
    normed_vector = (p1lp1m_norm + p2lp2m_norm.values + p3lp3m_norm.values) / 3

    return p1, normed_vector


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


def mirror_file_both_sets(dataset_l, dataset_r, dataset_l_for_plane, dataset_r_for_plane):
    if dataset_l_for_plane.empty and dataset_r_for_plane.empty:
        dataset_l_for_plane = dataset_l
        dataset_r_for_plane = dataset_r
    a, b, c, d = get_a_b_c_d(dataset_l_for_plane, dataset_r_for_plane)
    dataset_left = pd.DataFrame(columns=dataset_l.columns)

    for index, row in dataset_l.iterrows():
        mirrored_w = calculate_coordinates_of_mirrored_point(a, b, c, d, row[0], row[1], row[2])
        mirrored_e = calculate_coordinates_of_mirrored_point(a, b, c, d, row[3], row[4], row[5])
        mirrored_s = calculate_coordinates_of_mirrored_point(a, b, c, d, row[6], row[7], row[8])
        dataset_left.at[index, 0:3] = mirrored_w
        dataset_left.at[index, 3:6] = mirrored_e
        dataset_left.at[index, 6:9] = mirrored_s
    return dataset_left
