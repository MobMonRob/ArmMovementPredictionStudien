import os
from tkinter import *

from ArmMovementPredictionStudien.Preprocessing.utils.utils import open_dataset_numpy
from ArmMovementPredictionStudien.Preprocessing.visualisation.visualise_files import visualise
import matplotlib.pyplot as plt

first = True
file_list = os.listdir("../../DATA/0_raw/")

counter = 1090


def write_in_good():
    write(file_list[counter], "good")


def write_in_bad():
    write(file_list[counter], "bad")


def write(file, good_or_bad):
    plt.close('all')
    if good_or_bad == "good":
        database = open("./good_files.csv", 'a')
    elif good_or_bad == "bad":
        database = open("./bad_files.csv", 'a')
    else:
        raise Exception("Enter good or bad")
    length = len(open_dataset_numpy(file, "../../DATA/0_raw/"))
    database.write(f"{file};{length}\n")
    database.close()

    show_file()


def show_file():
    global counter
    print(counter)
    counter += 1
    visualise(file_selection=file_list[counter], pick_random_file=False)


if __name__ == "__main__":
    master = Tk()
    master.geometry("200x80+0+0")
    good_button = Button(master, text="Good", width=10, bg="green", command=write_in_good)
    bad_button = Button(master, text="Bad", width=10, bg="red", command=write_in_bad)
    good_button.pack(side="left")
    bad_button.pack(side="right")
    if first:
        show_file()
        first = False
    mainloop()
