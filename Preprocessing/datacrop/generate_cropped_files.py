import os
from dataTest import crop_data

for file in os.listdir("./data"):
    cropped_dataset = crop_data.crop_dataset_position(file, joint_type='w', threshold=0.01)
    new_filename = "./data_cropped/" + file.replace("takeover", "cropped")
    cropped_dataset.to_csv(path_or_buf=new_filename, sep=';', index=False, float_format='%.4f', na_rep='NaN')
