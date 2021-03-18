import os

from ArmMovementPredictionStudien.Preprocessing.smooth import smooth_data_utils

directory = "../../DATA/1_interpolated/"

for file in os.listdir(directory):
    smoothed_dataset = smooth_data_utils.generate_smooth_dataframe(file, directory, window=5)
    new_filename = "../../DATA/2_smoothed/" + file.replace("interpolated", "smoothed")
    smoothed_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
