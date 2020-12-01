from pandas import read_csv
import numpy

def readPos(filename):
    data = read_csv(filename, sep=",")
    return numpy.array(data)

def readKO(filename):
    raw = read_csv(filename, encoding="ISO-8859-1")
    all = list(map(lambda x: list(filter(lambda y: y != '', x.split(" "))),
                   list(numpy.array(raw).astype(str)[:, 0])))
    lengths = list(map(len, all))
    rawkolista = all[1:lengths.index(3)]
    others = all[all.index(['Sinkor', 'och', 'slaktkor', 'på', 'bete'])+3:-1]
    def insertNull(x):
        if len(x) == 7:
            x.insert(2, 'NULL')
        return x
    kolista = list(map(insertNull, rawkolista))
    sinld = list(filter(lambda x: x[2] == 'SINLD', others))
    skaut = list(filter(lambda x: x[2] =='SKAUT', others))

# 11 + 40
    return skaut

names = ["KO", "RESP", "TAG", "GR", "STAT", "LAKT", "KALVN", "DIM"]
ko = readKO("data/info/KO info 200921.txt")
for i in ko:
    print(i)