import pandas as pd
from pandas.testing import assert_frame_equal

from dataTest import crop_data


def test_crop_dataset():
    data = pd.DataFrame([[1, 1, 1], [1, 3, 4], [3, 6, 2], [4, 2, 7], [1, 2, 2]])
    expected = pd.DataFrame([[1, 3, 4], [3, 6, 2], [4, 2, 7]], index=[1, 2, 3])

    result = crop_data.crop_dataset_velocity(data, threshold=0.5)
    assert_frame_equal(result, expected, check_index_type=False)


def test_round_velocity_below_threshold_to_zero():
    data = pd.DataFrame([[1, 4, 1], [1, 3, 4], [3, 6, 2], [4, 2, 7], [1, 2, 4]])
    expected = pd.DataFrame([[0, 4, 0], [0, 3, 4], [3, 6, 0], [4, 0, 7], [0, 0, 4]])

    result = crop_data.round_velocity_below_threshold_to_zero(data, threshold=0.5)
    assert_frame_equal(result, expected, check_index_type=False)


def test_find_nearest_minima_from_maximum():
    data = pd.DataFrame([[1, 1, 1], [1, 3, 4], [3, 6, 2], [4, 2, -7], [1, 2, 2]])
    expected = [1, 3]

    result = crop_data.find_nearest_minima_from_maximum(data, threshold=0.5)
    assert result == expected


def test_find_maximum_velocity_of_single_dimension():
    data = pd.DataFrame([[-10, 1, 1], [1, 3, 4], [3, 6, 2], [4, 2, -7], [1, 2, 2]])
    expected_x = pd.DataFrame(data={"index_v_max": [0], "v_max": [10]})
    expected_y = pd.DataFrame(data={"index_v_max": [2], "v_max": [6]})
    expected_z = pd.DataFrame(data={"index_v_max": [3], "v_max": [7]})

    result_x = crop_data.find_maximum_velocity_of_single_dimension(data, dimension='x')
    result_y = crop_data.find_maximum_velocity_of_single_dimension(data, dimension='y')
    result_z = crop_data.find_maximum_velocity_of_single_dimension(data, dimension='z')

    assert_frame_equal(result_x, expected_x, check_index_type=False)
    assert_frame_equal(result_y, expected_y, check_index_type=False)
    assert_frame_equal(result_z, expected_z, check_index_type=False)
