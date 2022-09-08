# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
import time

import numpy as np


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    a = np.random.random(1000000)
    b = np.random.random(1000000)
    tic = time.time()
    a = np.dot(a, b)
    tie = time.time()
    print(f"let's see the time:" + str(1000 * (tie - tic)) + "ms")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # print_hi('PyCharm')
    k = np.random.randn(5)
    print(k.shape)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
