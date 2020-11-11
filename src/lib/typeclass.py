import numpy
import datetime

def timeConvert(time):
    timeFormat = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.datetime.fromtimestamp(time / 1000.0).strftime(timeFormat)


def insertWithFields(database, vals, type, fields):
    print("Inserting data...")
    print(vals[0])
    maxLen = len(vals)
    startIdx = 0
    endIdx = 0
    step = 100000
    while endIdx < maxLen:
        print("All records: ", startIdx, "/", maxLen, "  Percentage: ", startIdx / maxLen * 100, "%")
        if startIdx + step > maxLen:
            endIdx = maxLen
        else:
            endIdx += step
        print(startIdx, endIdx)
        cursor = database.cursor()
        statement = "INSERT INTO " + type + fields
        cursor.executemany(statement, vals[startIdx:endIdx])
        database.commit()
        cursor.close()
        startIdx = endIdx

def commonConvert(data, tableNames):
    reformated = numpy.column_stack(data)

    vals = {}
    for name in tableNames:
        # print("preparing...", name)
        mask = reformated[:, 0] == name
        tmp = reformated[mask][:, 1:]

        _, idx = numpy.unique(tmp[:, 1], return_index=True)
        dupNum = len(tmp) - len(idx)
        if dupNum != 0:
            print("duplicated number: ", dupNum)
        vals[name] = tuple(map(tuple, tmp[numpy.sort(idx), ]))
        # vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
    return vals
    #
    #
    # vals = {}
    # for name in tableNames:
    #     print("preparing...", name)
    #     mask = reformated[:, 0] == name
    #     vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
    # return vals


dateVec = numpy.vectorize(timeConvert)

class FA:
    def __init__(self):
        self.type = "FA"
        self.fields = " (tag_str, measure_time, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        reformated = numpy.column_stack((data[:, 2], dateVec(data[:, 3]), data[:, 4:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, vals):
        insertWithFields(database, vals, self.type, self.fields)

class PA:
    def __init__(self):
        self.type = "PA"
        self.fields = " (tag_str, start_time, end_time, posX, posY, posZ, activity_type, distance)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        reformated = numpy.column_stack((data[:, 2], dateVec(data[:, 3]), dateVec(data[:, 4]), data[:, 5:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, vals):
        insertWithFields(database, vals, self.type, self.fields)

# PAA: type, t1, interval, act, dis, period, dur
# PAA,2426227,00250573,1600646400000,600000,2,1290,16,228139
# 0   1       2        3             4      5 6    7  8
class PAA:
    def __init__(self):
        self.type = "PAA"
        self.fields = " (tag_str, measure_time, interv, activity_type, distance, period, duration)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        # reformated = (nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), data[:, 4:])
        reformated = numpy.column_stack((data[:, 2], dateVec(data[:, 3]), data[:, 4:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, vals):
        insertWithFields(database, vals, self.type, self.fields)


# PC,2432144,00251C90,1600646400756,1600646400756,2835,2681,198
class PC:
    def __init__(self):
        self.type = "PC"
        self.fields = " (tag_str, start_time, end_time, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        reformated = numpy.column_stack((data[:, 2], dateVec(data[:, 3]), dateVec(data[:, 4]), data[:, 5:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, vals):
        insertWithFields(database, vals, self.type, self.fields)