from pandas import read_csv
import numpy as np

def readPos(filename):
    data = read_csv(filename, sep=",")
    return np.array(data)