import numpy
import datetime

def timeConvert(time):
    timeFormat = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.datetime.fromtimestamp(time / 1000.0).strftime(timeFormat)

#
#
# def insertPCRecord(tableName, database, val):
#     cursor = database.cursor()
#     statement = "INSERT INTO "+tableName+\
#                 " (type, time1, time2, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s)"
#     cursor.executemany(statement, val)
#     database.commit()
#     cursor.close()
#
# def insertPARecord(tableName, database, val):
#     cursor = database.cursor()
#     statement = "INSERT INTO "+tableName+\
#                 " (type, time1, time2, posX, posY, posZ, act, distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
#     cursor.executemany(statement, val)
#     database.commit()
#     cursor.close()
#
# def insertPAARecord(tableName, database, val):
#     cursor = database.cursor()
#     statement = "INSERT INTO "+tableName+\
#                 " (type, time1, interval, activity, distance, period, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)"
#     cursor.executemany(statement, val)
#     database.commit()
#     cursor.close()

class FA:
    def __init__(self):
        self.type = "FA"

    def convert(self, data, tableNames):
        nameVec = numpy.vectorize(lambda x: "`" + x + "`")
        dateVec = numpy.vectorize(timeConvert)
        reformated = numpy.column_stack((nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), data[:, 4:]))

        vals = {}
        for name in tableNames:
            print("preparing...", name)
            mask = reformated[:, 0] == name
            vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
        return vals

    def insert(self, database, vals):
        for tableName in vals:
            print("Inserting ", tableName)
            cursor = database.cursor()
            statement = "INSERT INTO " + tableName + " (type, time1, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s)"
            cursor.executemany(statement, vals[tableName])
            database.commit()
            cursor.close()

class PA:
    def __init__(self):
        self.type = "PA"

    def convert(self, data, tableNames):
        nameVec = numpy.vectorize(lambda x: "`" + x + "`")
        dateVec = numpy.vectorize(timeConvert)
        reformated = numpy.column_stack((nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), dateVec(data[:, 4]),
                                         data[:, 5:]))

        vals = {}
        for name in tableNames:
            print("preparing...", name)
            mask = reformated[:, 0] == name
            vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
        return vals

    def insert(self, database, vals):
        for tableName in vals:
            print("Inserting ", tableName)
            cursor = database.cursor()
            statement = "INSERT INTO " + tableName + \
                        " (type, time1, time2, posX, posY, posZ, act, dist) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.executemany(statement, vals[tableName])
            database.commit()
            cursor.close()