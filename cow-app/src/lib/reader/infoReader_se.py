from pandas import read_csv
import numpy as np


def readKO(filename):
    raw = read_csv(filename, encoding="ISO-8859-1")
    all = list(map(lambda x: list(filter(lambda y: y != '', x.split(" "))),
                   list(np.array(raw).astype(str)[:, 0])))
    lengths = list(map(len, all))
    # raw kolista data
    rawkolista = all[1:lengths.index(3)]
    # info about cows that are dried off / to be slaughtered
    others = all[all.index(['Sinkor', 'och', 'slaktkor', 'på', 'bete'])+3:-1]
    # kolista handler function to add NULL for missing values
    def kolistaHandle(x):
        if len(x) == 7:
            x.insert(2, 'NULL')
        return x[:8]
    kolista = list(map(kolistaHandle, rawkolista))
    # raw data of dried off cows
    rawsinld = list(filter(lambda x: x[2] == 'SINLD', others))
    def sinldHandle(x):
        if len(x) > 13:
            n = len(x)-13
            x = x[:9]+[' '.join(x[9:10+n])]+x[10+n:]
        return x
    sinld = list(map(sinldHandle, rawsinld))
    # raw data of cows to be slaughtered
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
    # return two parts in numpy array
    return np.array(kolista), np.array(skaut+sinld)


def readHealth(filename):
    # read health data from files and return results in numpy array
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
    return np.array(lines)


# Reads "Avkastn" file and returns a list of lists containing CowID and 15 production records as 1 string
def readAvkastfile(filename):
    file1 = open(filename, 'r', errors='ignore', encoding="ISO-8859-1")
    lines = file1.readlines()
    file1.close()
    records = []
    for line in lines[4:-4]:
        line = line.split()
        number_strings = [str(num) for num in line[3:18]]
        other_string = " ".join(number_strings)
        record = [line[0], "production", other_string]
        records.append(record)
    return records


# Reads "Mjolkplats" file and returns a list of lists containing CowID and 15 milkings (station and time) as 1 string
def readMjolkplatsfile(filename):
    file1 = open(filename, 'r', errors='ignore', encoding="ISO-8859-1")
    lines = file1.readlines()
    file1.close()
    records = []
    for line in lines[5:-4]:
        line = line.split()
        number_strings = [str(num) for num in line[3:33]]
        other_string = " ".join(number_strings)
        record = [line[0], "time", other_string]
        records.append(record)
    return records
