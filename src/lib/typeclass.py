import numpy
import datetime

def timeConvert(time):
    timeFormat = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.datetime.fromtimestamp(time / 1000.0).strftime(timeFormat)

def insertWithFields(database, vals, fields):
    for tableName in vals:
        # print("Inserting ", tableName)
        cursor = database.cursor()
        statement = "INSERT INTO " + tableName + fields
        cursor.executemany(statement, vals[tableName])
        database.commit()
        cursor.close()

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


nameVec = numpy.vectorize(lambda x: "`" + x + "`")
dateVec = numpy.vectorize(timeConvert)

class FA:
    def __init__(self):
        self.type = "FA"
        self.fields = " (type, time1, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s)"

    def convert(self, data, tableNames):
        reformated = (nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), data[:, 4:])
        return commonConvert(reformated, tableNames)

    def insert(self, database, vals):
        insertWithFields(database, vals, self.fields)

class PA:
    def __init__(self):
        self.type = "PA"
        self.fields = " (type, time1, time2, posX, posY, posZ, act, dist) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data, tableNames):
        reformated = (nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), dateVec(data[:, 4]),
                                         data[:, 5:])
        #
        # vals = {}
        # for name in tableNames:
        #     print("preparing...", name)
        #     mask = reformated[:, 0] == name
        #     tmp = reformated[mask][:, 1:]
        #     _, idx = numpy.unique(tmp[:, 1], return_index=True)
        #     vals[name] = tuple(map(tuple, tmp[numpy.sort(idx), ]))
        #     #vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
        # return vals

        return commonConvert(reformated, tableNames)

    def insert(self, database, vals):
        insertWithFields(database, vals, self.fields)

# PAA: type, t1, interval, act, dis, period, dur
# PAA,2426227,00250573,1600646400000,600000,2,1290,16,228139
# 0   1       2        3             4      5 6    7  8
class PAA:
    def __init__(self):
        self.type = "PAA"
        self.fields = " (type, time1, intv, act, dist, per, dur) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data, tableNames):
        # nameVec = numpy.vectorize(lambda x: "`" + x + "`")
        # dateVec = numpy.vectorize(timeConvert)
        reformated = (nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), data[:, 4:])
        #
        # vals = {}
        # for name in tableNames:
        #     print("preparing...", name)
        #     mask = reformated[:, 0] == name
        #     tmp = reformated[mask][:, 1:]
        #     _, idx = numpy.unique(tmp[:, 1], return_index=True)
        #     vals[name] = tuple(map(tuple, tmp[numpy.sort(idx), ]))
        #     #vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
        # return vals
        return commonConvert(reformated, tableNames)

    def insert(self, database, vals):
        insertWithFields(database, vals, self.fields)

# PC,2432144,00251C90,1600646400756,1600646400756,2835,2681,198
class PC:
    def __init__(self):
        self.type = "PC"
        self.fields = " (type, time1, time2, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s)"

    def convert(self, data, tableNames):
        # nameVec = numpy.vectorize(lambda x: "`" + x + "`")
        # dateVec = numpy.vectorize(timeConvert)
        reformated = (nameVec(data[:, 2]), data[:, 0],
                                         dateVec(data[:, 3]), dateVec(data[:, 4]), data[:, 5:])
        #
        # vals = {}
        # for name in tableNames:
        #     print("preparing...", name)
        #     mask = reformated[:, 0] == name
        #     tmp = reformated[mask][:, 1:]
        #     _, idx = numpy.unique(tmp[:, 1], return_index=True)
        #     vals[name] = tuple(map(tuple, tmp[numpy.sort(idx), ]))
        #     #vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
        # return vals
        return commonConvert(reformated, tableNames)

    def insert(self, database, vals):
        insertWithFields(database, vals, self.fields)