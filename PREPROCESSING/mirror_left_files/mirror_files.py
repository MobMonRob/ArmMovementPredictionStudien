import os
from shutil import copy
from traceback import print_exc

from ArmMovementPredictionStudien.PREPROCESSING.mirror_left_files.mirror_left_files_plane_both_sets import \
    mirror_file_both_sets
from ArmMovementPredictionStudien.PREPROCESSING.mirror_left_files.mirror_left_files_plane_self import \
    mirror_file_one_set
from ArmMovementPredictionStudien.PREPROCESSING.mirror_left_files.mirror_left_files_utils import \
    make_datasets_the_same_length
from ArmMovementPredictionStudien.PREPROCESSING.utils.utils import open_dataset_pandas
from scipy import stats


directory = "../../DATA/4_prefiltered/"
filelist_left = []
filelist_directory = os.listdir(directory)

for file in filelist_directory:
    if "_L" in file:
        filelist_left.append(file)
    if "_R" in file:
        filename = file.replace("prefiltered", "mirrored")
        copy(directory + file, "../../DATA/5_mirrored/" + filename)

sum_plane_both_sets = 0
sum_plane_self = 0
sum_plane_self_error = 0
files_with_both_hands = []
files_with_error = []
filelength_both_hands = []

for file in filelist_left:
    filename_right = file.replace("_L", "_R")
    dataset_l = open_dataset_pandas(file, directory=directory)
    if filename_right in filelist_directory:
        dataset_r = open_dataset_pandas(filename_right, directory)
        try:
            dataset_l_for_plane, dataset_r_for_plane = make_datasets_the_same_length(file, directory)
            dataset_left = mirror_file_both_sets(dataset_l, dataset_r, dataset_l_for_plane, dataset_r_for_plane)
            sum_plane_both_sets += 1
            files_with_both_hands.append(file)
            filelength_both_hands.append(len(dataset_l_for_plane))
        except (EOFError, ValueError):  # Right hand has only NaN after shifting or left hand is completely shit
            #  print_exc()
            dataset_left = mirror_file_one_set(dataset_l)
            sum_plane_self_error += 1
            files_with_error.append(file)
            pass
    else:
        dataset_left = mirror_file_one_set(dataset_l)
        sum_plane_self += 1
    new_filename = "../../DATA/5_mirrored/" + file.replace("prefiltered", "mirrored")
    dataset_left.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')

    sum_all = sum_plane_self + sum_plane_self_error + sum_plane_both_sets
    if sum_all%20 == 0:
        print(f"[{sum_all}/{len(filelist_left)}]")

print(f"Both hands could be used: {sum_plane_both_sets}\nOne Hand could be used: {sum_plane_self}\n"
      f"One Hand with errors: {sum_plane_self_error}")
print(f"Both_hand_files: {files_with_both_hands}")
print(f"Error_files: {files_with_error}")
print(stats.describe(filelength_both_hands))
