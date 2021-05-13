import os
from random import shuffle

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from numpy import gradient, sqrt, sin, cos
from numpy.linalg import norm
from scipy.optimize import leastsq, curve_fit

random_file = False
file_selected = "20200403139_filtered_R.csv"
# file_selected = "20200423131_filtered_L.csv"
mjm = "mjm_curved_full"

ROOT_DIR = os.path.dirname(__file__) + "/../"


def calculate_trajectory(file_selection=file_selected, pick_random_file=random_file, end_point=np.array([0, 0, 0]),
                         lastindex=-1, method=mjm):
    base_directory = ROOT_DIR + "DATA/"
    filtered_directory = base_directory + "7_filtered/"

    if pick_random_file:
        all_files = os.listdir(filtered_directory)
        shuffle(all_files)
        file_selection = all_files[0]
    print(file_selection)

    csv_file = filtered_directory + file_selection
    dataset_original = pd.read_csv(csv_file, sep=";")

    startpoint = dataset_original.iloc[0, 0:3]
    if abs(end_point[0]) < 0.001 and abs(end_point[1]) < 0.001 and abs(end_point[2]) < 0.001:
        endpoint = dataset_original.iloc[-1, 0:3]
    else:
        endpoint = end_point
    if lastindex == -1:
        last_index = len(dataset_original) - 1
    else:
        last_index = lastindex

    df_orig = dataset_original.iloc[:, 0:3]
    df_orig_v = gradient(df_orig, axis=0)
    df_orig_a = gradient(df_orig_v, axis=0)

    if method == "mmjm":
        df_mjm = calculate_modified_minimum_jerk(df_orig, endpoint, last_index)
    elif method == "mjm":
        df_mjm = calculate_minimum_jerk(startpoint, endpoint, last_index)
    elif method == "mjm_curved":
        df_mjm = calculate_minimum_jerk_curved(df_orig.iloc[0:85, :], endpoint, last_index)  # Input of first x points
    elif method == "mjm_curved_full":
        df_mjm = calculate_minimum_jerk_curved_full(df_orig.iloc[0:85, :], endpoint,
                                                    last_index)  # Input of first x points
    elif method == "mjm_pmv":
        df_mjm = calculate_minimum_jerk_with_pmv(startpoint, endpoint, df_orig_v[0], df_orig_v[-1], df_orig_a[0],
                                                 df_orig_a[-1], last_index)
    else:
        raise Exception("no.")
    df_mjm_v = gradient(df_mjm, axis=0)
    df_mjm_a = gradient(df_mjm_v, axis=0)

    visualise(df_orig, df_orig_v, df_orig_a, df_mjm, df_mjm_v, df_mjm_a)
    return df_mjm, file_selection


def calculate_minimum_jerk(startpoint, endpoint, last_index):
    dataset_mjm = pd.DataFrame()
    for index in range(0, last_index + 1):
        tau = index / last_index
        point = startpoint + (startpoint - endpoint) * (15 * (tau ** 4) - 6 * (tau ** 5) - 10 * (tau ** 3))
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)
    return dataset_mjm


def calculate_minimum_jerk_with_pmv(startpoint, endpoint, startpoint_v, endpoint_v, startpoint_a, endpoint_a,
                                    last_index):
    dataset_mjm = pd.DataFrame()

    d = last_index
    a_0 = startpoint
    a_1 = startpoint_v
    a_2 = 0.5 * startpoint_a
    a_3 = - 10 / d ** 3 * startpoint - 6 / d ** 2 * startpoint_v - 3 / d * startpoint_a + 10 / d ** 3 * endpoint - 4 / d ** 2 * endpoint_v + 1 / d * endpoint_a
    a_4 = 15 / d ** 4 * startpoint + 8 / d ** 3 * startpoint_v + 3 / d ** 2 * startpoint_a - 15 / d ** 4 * endpoint + 7 / d ** 3 * endpoint_v - 1 / d ** 2 * endpoint_a
    a_5 = - 6 / d ** 5 * startpoint - 3 / d ** 4 * startpoint_v - 1 / d ** 3 * startpoint_a + 6 / d ** 5 * endpoint - 3 / d ** 4 * endpoint_v + 1 / d ** 3 * endpoint_a

    for index in range(0, last_index + 1):
        point = a_0 + a_1 * index + a_2 * index ** 2 + a_3 * index ** 3 + a_4 * index ** 4 + a_5 * index ** 5
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)
    return dataset_mjm


def calculate_minimum_jerk_curved(startmovement, endpoint, last_index):
    dataset_mjm = pd.DataFrame.copy(startmovement)

    t_1 = startmovement.index[-1]
    t_f = last_index
    x_0 = startmovement.iloc[0, 0:3]
    x_1 = startmovement.iloc[t_1]
    x_f = endpoint

    tau_1 = t_1 / t_f
    c = 1 / (t_f ** 5 * tau_1 ** 2 * (1 - tau_1) ** 5) * (
            (x_f - x_0) * (300 * tau_1 ** 5 - 1200 * tau_1 ** 4 + 1600 * tau_1 ** 3)
            + tau_1 ** 2 * (-720 * x_f + 120 * x_1 + 600 * x_0) + (x_0 - x_1) * (300 * tau_1 - 200))
    pi = 1 / (t_f ** 5 * tau_1 ** 5 * (1 - tau_1) ** 5) * (
            (x_f - x_0) * (120 * tau_1 ** 5 - 300 * tau_1 ** 4 + 200 * tau_1 ** 3) - 20 * (x_1 - x_0))
    for t in range(t_1 + 1, t_f + 1):
        tau = t / t_f
        point = t_f ** 5 / 720 * (pi * (tau_1 ** 4 * (15 * tau ** 4 - 30 * tau ** 3 + 30 * tau - 15) + tau_1 ** 3 * (
                -30 * tau ** 4 + 80 * tau ** 3 - 60 * tau ** 2 + 10))
                                  + c * (-6 * tau ** 5 + 15 * tau ** 4 - 10 * tau ** 3 + 1)) + x_f
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)
    return dataset_mjm


def calculate_minimum_jerk_curved_full(startmovement, endpoint, last_index):
    t_1 = get_farest_distant_point(startmovement)
    t_f = last_index
    x_0 = startmovement.iloc[0, 0:3]
    x_1 = startmovement.iloc[t_1]
    x_f = endpoint

    dataset_mjm = pd.DataFrame()

    tau_1 = t_1 / t_f
    c = 1 / (t_f ** 5 * tau_1 ** 2 * (1 - tau_1) ** 5) * (
            (x_f - x_0) * (300 * tau_1 ** 5 - 1200 * tau_1 ** 4 + 1600 * tau_1 ** 3)
            + tau_1 ** 2 * (-720 * x_f + 120 * x_1 + 600 * x_0) + (x_0 - x_1) * (300 * tau_1 - 200))
    pi = 1 / (t_f ** 5 * tau_1 ** 5 * (1 - tau_1) ** 5) * (
            (x_f - x_0) * (120 * tau_1 ** 5 - 300 * tau_1 ** 4 + 200 * tau_1 ** 3) - 20 * (x_1 - x_0))

    for t in range(0, t_1 + 1):
        tau = t / t_f
        point = t_f ** 5 / 720 * (pi * (tau_1 ** 4 * (15 * tau ** 4 - 30 * tau ** 3) + tau_1 ** 3 * (
                 80 * tau ** 3 - 30 * tau ** 4) - 60 * tau ** 3 * tau_1 **2 + 30 * tau ** 4 * tau_1 - 6 * tau ** 5)
                                  + c * (15 * tau ** 4 - 10 * tau ** 3 - 6 * tau ** 5)) + x_0
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)

    for t in range(t_1 + 1, t_f + 1):
        tau = t / t_f
        point = t_f ** 5 / 720 * (pi * (tau_1 ** 4 * (15 * tau ** 4 - 30 * tau ** 3 + 30 * tau - 15) + tau_1 ** 3 * (
                -30 * tau ** 4 + 80 * tau ** 3 - 60 * tau ** 2 + 10))
                                  + c * (-6 * tau ** 5 + 15 * tau ** 4 - 10 * tau ** 3 + 1)) + x_f
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)
    return dataset_mjm


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
    return max_ind


def visualise(dataset_original, orig_v, orig_a, dataset_mjm, mjm_v, mjm_a):
    dataset_error = dataset_original - dataset_mjm
    err_v = orig_v - mjm_v
    err_a = orig_a - mjm_a
    fig, axs = plt.subplots(2, 3)
    axs[0, 0].plot(range(0, len(dataset_original)), dataset_original)
    axs[0, 0].set_title("Original Trajectory")
    axs[0, 0].set_xlabel('Frame')
    axs[0, 0].set_ylabel('Position in mm')
    axs[0, 1].plot(range(0, len(orig_v)), orig_v)
    axs[0, 1].set_title("Original Trajectory Velocity")
    axs[0, 1].set_xlabel('Frame')
    axs[0, 1].set_ylabel('Velocity in mm/Frame')
    axs[0, 2].plot(range(0, len(orig_a)), orig_a)
    axs[0, 2].set_title("Original Trajectory Acceleration")
    axs[0, 2].set_xlabel('Frame')
    axs[0, 2].set_ylabel('Acceleration in mm/frame²')
    axs[1, 0].plot(range(0, len(dataset_mjm)), dataset_mjm)
    axs[1, 0].set_title("Minimum Jerk Model")
    axs[1, 0].set_xlabel('Frame')
    axs[1, 0].set_ylabel('Position in mm')
    axs[1, 1].plot(range(0, len(mjm_v)), mjm_v)
    axs[1, 1].set_title("Minimum Jerk Model Velocity")
    axs[1, 1].set_xlabel('Frame')
    axs[1, 1].set_ylabel('Velocity in mm/Frame')
    axs[1, 2].plot(range(0, len(mjm_a)), mjm_a)
    axs[1, 2].set_title("Minimum Jerk Model Acceleration")
    axs[1, 2].set_xlabel('Frame')
    axs[1, 2].set_ylabel('Acceleration in mm/frame²')
    # axs[2, 0].plot(range(0, len(dataset_error)), dataset_error)
    # axs[2, 0].set_title("Error")
    # axs[2, 0].set_xlabel('Frame')
    # axs[2, 0].set_ylabel('Position in mm')
    # axs[2, 1].plot(range(0, len(err_v)), err_v)
    # axs[2, 1].set_title("Error Velocity")
    # axs[2, 1].set_xlabel('Frame')
    # axs[2, 1].set_ylabel('Velocity in mm/Frame')
    # axs[2, 2].plot(range(0, len(err_a)), err_a)
    # axs[2, 2].set_title("Error Acceleration")
    # axs[2, 2].set_xlabel('Frame')
    # axs[2, 2].set_ylabel('Acceleration in mm/frame²')
    fig.legend(['x', 'y', 'z'], loc='upper left')
    # fig.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0.)
    plt.show()


def calculate_modified_minimum_jerk(early_stage, endpoint, last_index):
    early_stage_x = early_stage.iloc[0:80, 0]
    early_stage_y = early_stage.iloc[0:80, 1]
    early_stage_z = early_stage.iloc[0:80, 2]

    xDatax = np.array(range(len(early_stage_x)))
    result_x, pcov = curve_fit(f=four, xdata=xDatax, ydata=early_stage_x)
    xDatay = np.array(range(len(early_stage_y)))
    result_y, pcov = curve_fit(f=four, xdata=xDatay, ydata=early_stage_y)
    xDataz = np.array(range(len(early_stage_z)))
    result_z, pcov = curve_fit(f=four, xdata=xDataz, ydata=early_stage_z)

    startpoint = early_stage.iloc[0, :]
    dataset_mjm = pd.DataFrame()
    for index in range(0, last_index + 1):
        tau = index / last_index

        fourier = np.array([four(index, result_x[0], result_x[1], result_x[2], result_x[3]),
                            four(index, result_y[0], result_y[1], result_y[2], result_y[3]),
                            four(index, result_z[0], result_z[1], result_z[2], result_z[3]), ])
        point = startpoint + (startpoint - endpoint) * (15 * (tau ** 4) - 6 * (tau ** 5) - 10 * (tau ** 3)) + fourier
        dataset_mjm = dataset_mjm.append(point, ignore_index=True)
    return dataset_mjm


def four(x, a, b, c, d):
    w = 2 * np.pi / 111  # t_f
    e = -b - d
    return (a * sin(w * x) + b * cos(w * x) + c * sin(2 * w * x) + d * cos(2 * w * x) + e) / w


def write_to_csv(dataset, file_selection=file_selected):
    new_filename = f"./Prediction/{file_selection.replace('filtered', 'predicted')}"
    dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')


if __name__ == "__main__":
    # pred, name = calculate_trajectory(file_selected, random_file)
    # write_to_csv(pred, name)

    end = np.array([463.33291545, -293.09159033, 675.24663569])
    dataset_pred, filename = calculate_trajectory(file_selection="20200403155_filtered_R.csv", end_point=end, lastindex=111)
    write_to_csv(dataset_pred, filename)
