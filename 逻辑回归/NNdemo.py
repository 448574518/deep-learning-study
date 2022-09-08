import numpy as np
import h5py

dateset = h5py.File('datasets/train_catvnoncat.h5', "r")

tran_set_x = np.array(dateset["train_set_x"][:])
tran_set_y = np.array(dateset["train_set_y"][:])

print(tran_set_y.shape)
# print("train_set_y:" + tran_set_y)

