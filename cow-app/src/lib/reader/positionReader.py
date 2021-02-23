from pandas import read_csv
import numpy as np

def readPos(filename, nrows, skiprows=0):
    data = read_csv(filename, sep=",", skiprows=skiprows, nrows=nrows, header=None)
    return np.array(data)