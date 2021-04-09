import os

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas, open_dataset_numpy
import pandas as pd

def write_endpoints_to_csv(date, left_right, directory):
    if date == "0305":
        if left_right == "R":
            file_list = file_list_0305_R
        elif left_right == "L":
            file_list = file_list_0305_L
        else:
            raise Exception(f"[L]eft or [R]ight")
    elif date == "0403":
        if left_right == "R":
            file_list = file_list_0403_R
        elif left_right == "L":
            file_list = file_list_0403_L
        else:
            raise Exception(f"[L]eft or [R]ight")
    elif date == "0423":
        if left_right == "R":
            file_list = file_list_0423_R
        elif left_right == "L":
            file_list = file_list_0403_L
        else:
            raise Exception(f"[L]eft or [R]ight")
    else:
        raise Exception(f"Date '{date}' not available.")

    for file in file_list:
        dataset = open_dataset_pandas(file, directory)
        endpoint = dataset.iloc[-1, 0:3]

        endpoint_file = open(endpoint_directory + "endpoints_" + date + "_" + left_right + ".csv", 'a')
        endpoint_file.write(f"{endpoint.iloc[0]};{endpoint.iloc[1]};{endpoint.iloc[2]}\n")
        endpoint_file.close()


directory = "../0_raw/"
endpoint_directory = "./"
file_list_directory = os.listdir(directory)

file_list_0305_R = []
file_list_0403_R = []
file_list_0423_R = []
file_list_0305_L = []
file_list_0403_L = []
file_list_0423_L = []

for file in file_list_directory:
    if "20200305" in file:
        if "_R" in file:
            file_list_0305_R.append(file)
        else:
            file_list_0305_L.append(file)
    elif "20200403" in file:
        if "_R" in file:
            file_list_0403_R.append(file)
        else:
            file_list_0403_L.append(file)
    elif "20200423" in file:
        if "_R" in file:
            file_list_0423_R.append(file)
        else:
            file_list_0423_L.append(file)
    else:
        raise Exception(f"File '{file}' not assignable.")

write_endpoints_to_csv("0305", "L", directory)



