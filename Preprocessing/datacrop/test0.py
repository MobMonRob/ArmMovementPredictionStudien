import os
from random import shuffle
import matplotlib.pyplot as plt
import pandas as pd
import velocity
from dataTest import crop_data

cropped_files = os.listdir("./data_cropped")
shuffle(cropped_files)
selection = cropped_files[0:4]

counter = 0
x = [0, 1, 2, 3]
y = [0, 1, 2, 3]

for file in selection:
    data = velocity.calculate_velocity_vector_for_dataset(file, directory="./data_cropped/")
    data = pd.DataFrame(data)
    data = crop_data.calculate_velocity_of_trajectory(data)
    x[counter] = range(0, len(data))
    y[counter] = data
    counter += 1

fig, axs = plt.subplots(2, 2)
axs[0, 0].plot(x[0], y[0])
axs[0, 0].set_title(selection[0])
axs[0, 1].plot(x[1], y[1], 'tab:orange')
axs[0, 1].set_title(selection[1])
axs[1, 0].plot(x[2], y[2], 'tab:green')
axs[1, 0].set_title(selection[2])
axs[1, 1].plot(x[3], y[3], 'tab:red')
axs[1, 1].set_title(selection[3])

print(selection)
plt.show()

