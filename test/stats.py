from pandas import read_csv
import numpy


def read_data(filename):
    data = read_csv(filename, sep=",")
    return numpy.array(data)

def stats(data):
    stats = {}
    for i in data[:,1]:
        if stats.get(i) is None:
            stats[i] = 1
        else:
            stats[i] += 1
    return stats

path = "data/position/"
FA = read_data(path+"FA_20200921T000000UTC.csv")
PA = read_data(path+"PA_20200921T000000UTC.csv")
PAA = read_data(path+"PAA_20200921T000000UTC.csv")
PC = read_data(path+"PC_20200921T000000UTC.csv")

FAstats = stats(FA)