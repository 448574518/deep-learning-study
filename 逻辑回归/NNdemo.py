import numpy as np
import h5py

dateset = h5py.File('datasets/train_catvnoncat.h5', "r")
test_dataset = h5py.File('datasets/test_catvnoncat.h5', "r")
tran_set_x = np.array(dateset["train_set_x"][:])
tran_set_y = np.array(dateset["train_set_y"][:])

test_set_y = np.array((test_dataset["test_set_y"][:]))
test_set_y = test_set_y.reshape((1, test_set_y.shape[0]))

print(np.squeeze(test_set_y[:, 5]))
# print("train_set_y:" + tran_set_y)

