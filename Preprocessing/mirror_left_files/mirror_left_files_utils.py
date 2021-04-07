from pandas import isnull

from ArmMovementPredictionStudien.Preprocessing.truncate.truncate_data_utils import find_maximum_velocity_of_trajectory
from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_pandas
from ArmMovementPredictionStudien.Preprocessing.utils.velocity import calculate_velocity_of_trajectory, \
    generate_velocity_dataframe


def get_index_of_max_velocity(dataset_v):
    return find_maximum_velocity_of_trajectory(dataset_v)["index_v_max"].values[0]


def shift_trajectory(trajectory, index_from, index_to):
    index_shift = index_to - index_from
    shifted_trajectory = trajectory.shift(index_shift)
    return shifted_trajectory


def make_datasets_the_same_length(filename, directory):
    if "_L" in filename:
        filename_l = filename
        filename_r = filename.replace("_L", "_R")
    elif "_R" in filename:
        filename_r = filename
        filename_l = filename.replace("_R", "_L")
    else:
        raise Exception("Wrong filename")

    dataset_l = open_dataset_pandas(filename_l, directory)
    dataset_r = open_dataset_pandas(filename_r, directory)
    dataset_v_l = generate_velocity_dataframe(filename_l, directory)
    dataset_v_r = generate_velocity_dataframe(filename_r, directory)
    index_v_max_l = get_index_of_max_velocity(dataset_v_l)
    index_v_max_r = get_index_of_max_velocity(dataset_v_r)
    trajectory_l = calculate_velocity_of_trajectory(dataset_v_l)
    trajectory_r = calculate_velocity_of_trajectory(dataset_v_r)
    trajectory_r = shift_trajectory(trajectory_r, index_v_max_r, index_v_max_l)

    if trajectory_l.isnull().all():  # should not happen
        raise Exception(f"Every value in {filename_l} is NaN after shifting")
    if trajectory_r.isnull().all():
        raise EOFError(f"Every value in {filename_r} is NaN after shifting")

    index_start = 0
    index_end = 0
    if len(trajectory_r) > len(trajectory_l):
        loop_index_end = len(trajectory_l)
    else:
        loop_index_end = len(trajectory_r)

    for index in range(loop_index_end):
        if not isnull(trajectory_l[index]) and not isnull(trajectory_r[index]):
            index_start = index
            break
    for index in range(index_start, loop_index_end): # TODO: von hinten anfangen
        if isnull(trajectory_l[index]) or isnull(trajectory_r[index]):
            index_end = index - 1
            break
        index_end = index

    if index_end <= index_start:
        raise EOFError(f"Attention: {filename} has index_start at {index_end} and index_end at {index_end}")

    dataset_l = dataset_l.truncate(before=index_start, after=index_end).reset_index(drop=True)
    dataset_r = dataset_r.truncate(before=index_start, after=index_end).reset_index(drop=True)

    return dataset_l, dataset_r


# make_datasets_the_same_length("20200305291_truncated_L.csv", "../../DATA/3_truncated/")
