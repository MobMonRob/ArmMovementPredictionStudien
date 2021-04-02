import os
from shutil import copy

from ArmMovementPredictionStudien.Preprocessing.mirror_left_files.mirror_left_files_plane_both_sets import \
    mirror_file_both_sets
from ArmMovementPredictionStudien.Preprocessing.mirror_left_files.mirror_left_files_plane_self import \
    mirror_file_one_set
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas


directory = "../../DATA/3_truncated/"
filelist_left = []
filelist_directory = os.listdir(directory)

for file in filelist_directory:
    if "_L" in file:
        filelist_left.append(file)
    if "_R" in file:
        filename = file.replace("truncated", "mirrored")
        copy(directory + file, "../../DATA/4_mirrored/" + filename)

for file in filelist_left:
    dataset_l = open_dataset_pandas(file, directory=directory)
    filename_right = file.replace("_L", "_R")
    if filename_right in filelist_directory:
        dataset_r = open_dataset_pandas(filename_right, directory=directory)
        dataset_left = mirror_file_both_sets(dataset_l, dataset_r)
    else:
        dataset_left = mirror_file_one_set(dataset_l)
    new_filename = "../../DATA/4_mirrored/" + file.replace("truncated", "mirrored")
    dataset_left.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')