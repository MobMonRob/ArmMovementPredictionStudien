import os
from random import shuffle

from numpy import sqrt

from ArmMovementPredictionStudien.Preprocessing.utils.velocity import calculate_velocity_vector_for_dataset_filename, \
    calculate_velocity_vector_for_dataset

import matplotlib.pyplot as plt


def show_examples_of_acceleration(file="rand"):
    dir_int = "../../DATA/3_truncated/"
    if file == "rand":
        files = os.listdir(dir_int)
        shuffle(files)
        file = files[0]
    v_vector = calculate_velocity_vector_for_dataset_filename(file, dir_int)
    a_vector = calculate_velocity_vector_for_dataset(v_vector, filename=file)
    v_trajectory = sqrt(v_vector[:, 0] ** 2 + v_vector[:, 1] ** 2 + v_vector[:, 2] ** 2)
    a_trajectory = sqrt(a_vector[:, 0] ** 2 + a_vector[:, 1] ** 2 + a_vector[:, 2] ** 2) * 10
    plt.plot(v_trajectory, label=f"velocity")
    plt.plot(a_trajectory, label=f"acceleration*10")
    plt.title(file)
    print(file)
    plt.legend(loc='best')
    plt.show()


if __name__ == "__main__":
    # show_examples_of_acceleration("20200305296_truncated_R.csv")
    show_examples_of_acceleration('20200305033_truncated_R.csv')  # 75, 206
