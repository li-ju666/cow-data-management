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
    def kolistaHandle(x):
        if len(x) == 7:
            x.insert(2, 'NULL')
        return x[:8]
    kolista = list(map(kolistaHandle, rawkolista))
    rawsinld = list(filter(lambda x: x[2] == 'SINLD', others))
    def sinldHandle(x):
        if len(x) > 13:
            n = len(x)-13
            x = x[:9]+[' '.join(x[9:10+n])]+x[10+n:]
        return x
    sinld = list(map(sinldHandle, rawsinld))
    rawskaut = list(filter(lambda x: x[2] =='SKAUT', others))
    def skaultHandle(x):
        result = []+x[0:3]
        idx = 3
        if x[3] == '0':
            result.append('NULL')
            result.append(x[3])
            idx = 4
        else:
            result += x[3:5]
            idx = 5
        result += x[idx:idx+2]
        idx += 2
        if x[idx] == '0':
            result.append('NULL')
            result.append(x[idx])
            idx += 1
        else:
            result += x[idx:idx+2]
            idx += 2
        result.append(' '.join(x[idx:-2]))
        result += x[-2:]
        if result[-3] == '':
            result[-3] = 'NULL'
        result.insert(-2, 'NULL')

        return result

    skaut = list(map(skaultHandle, rawskaut))

    return numpy.array(kolista), numpy.array(skaut+sinld)

def readHealth(filename):
    file = open(filename, encoding="ISO-8859-1")
    raw = file.readlines()
    lines = []
    for i in raw:
        lines.append(i.split(sep=" "))
    def removeEmpty(x):
        return list(filter(lambda x: x != '' and x != '\n', x))
    lines = list(map(removeEmpty, lines))
    idx = lines.index(['nr', 'nr', 'dat', '7dag', '100dag', 'dag', 'datum', 'namn'])
    lines = lines[idx+1:]
    def healthHandle(x):
        result = x[:8]
        try:
            result.append(str(int(x[8])))
            idx = 9
        except:
            result.append("NULL")
            idx = 8
        result.append(' '.join(x[idx:]))
        return result
    lines = list(map(healthHandle, lines))
    return numpy.array(lines)

# all= readHealth("data/info/Översikt hälsotillstånd X 200921.txt")
# for i in all:
#      print(len(i))