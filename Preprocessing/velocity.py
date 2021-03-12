import os

from numpy import gradient, genfromtxt
import pandas as pd


def determine_left_or_right_dataset(filename):
    if 'RGrasp' in filename:
        return "R"
    if "LGrasp" in filename:
        return "L"
    return "X"


def open_dataset_pandas(filename):
    csv_file = "./data/" + filename
    return pd.read_csv(csv_file, sep=";")


def open_dataset_numpy(filename):
    csv_file = "./data/" + filename
    genfromtxt(csv_file, delimiter=";", skip_header=1)


def calculate_velocity_vector_for_dataset(filename):
    dataset = open_dataset_pandas(filename)
    return gradient(dataset.to_numpy(), axis=0)


def write_velocity_dataset_to_csv(filename):
    dataset_velocity = calculate_velocity_vector_for_dataset(filename)
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
    new_filename = "./data_velocity/" + filename.replace("takeover", "velocity")
    dataframe_velocity.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')


if __name__ == '__main__':
    for file in os.listdir("./data"):
        write_velocity_dataset_to_csv(file)
