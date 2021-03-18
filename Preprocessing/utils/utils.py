import pandas as pd
from numpy import genfromtxt


def open_dataset_pandas(filename, directory):
    csv_file = directory + filename
    return pd.read_csv(csv_file, sep=";")


def open_dataset_numpy(filename, directory):
    csv_file = directory + filename
    return genfromtxt(csv_file, delimiter=";", skip_header=1)
