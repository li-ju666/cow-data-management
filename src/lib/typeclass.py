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
        vals[name] = tuple(map(tuple, tmp[numpy.sort(idx),]))
        # vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))
    return vals


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


class KO:
    def __init__(self):
        self.type1 = "CowInfo"
        self.fields1 = " (cowID, insertDate, resp, grp, stat, lakt, kalvn_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.type2 = "DriedInfo"
        self.fields2 = " (cowID, insertDate, gp, avsinad, insem_date, sedan_insem, insem_tjur, forv_kalvn, " \
                       "tid_ins, tid_mellan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, kolista, dried, insertDate):
        print("Converting data")
        fileDate = datetime.datetime.strptime(insertDate, "%y%m%d")
        fileDate = fileDate.strftime("%y-%m-%d")
        def kalvnDate(x):
            try:
                a = datetime.datetime.strptime(x, "%d-%m-%y")
                return a.strftime("%Y-%m-%d")
            except:
                return 'NULL'
        kalvnVec = numpy.vectorize(kalvnDate)
        kolista = numpy.column_stack((kolista[:, 0], numpy.repeat(fileDate, len(kolista)), kolista[:, 1],
                                     kolista[:, 3:6], kalvnVec(kolista[:, 6])))

        dried = numpy.column_stack((dried[:, 0], numpy.repeat(fileDate, len(dried)), dried[:, 1],
                                    kalvnVec(dried[:, 3]), kalvnVec(dried[:, 7]), dried[:, 8:10],
                                    kalvnVec(dried[:, 10]), dried[:, 11:]))
        # def cleanNone(x):
        #     if x == 'None':
        #         return 1
        # NoneVec = numpy.vectorize(cleanNone)
        def removeNull(x):
            return tuple(map(lambda x: None if x == 'NULL' else x, x))
        return tuple(map(removeNull, kolista)), tuple(map(removeNull, dried))

    def insert(self, database, kolista, dried):
        insertWithFields(database, kolista, self.type1, self.fields1)
        insertWithFields(database, dried, self.type2, self.fields2)

class Health:
    def __init__(self):
        self.type = "HealthInfo"
        self.fields = " (cowID, insertDate, 7dag, 100dag, handelse_day, comments)" \
                      " VALUES (%s, %s, %s, %s, %s, %s)"

    def convert(self, data, insertDate):
        print("Converting data")
        print(data[0,4])
        print(data[0,5])
        fileDate = datetime.datetime.strptime(insertDate, "%y%m%d")
        fileDate = fileDate.strftime("%y-%m-%d")
        reformated = numpy.column_stack((data[:, 0], numpy.repeat(fileDate, len(data)),
                                         data[:, -4:]))
        def removeNull(x):
            return tuple(map(lambda x: None if x == 'NULL' else x, x))
        return tuple(map(removeNull, reformated))

    def insert(self, database, vals):
        insertWithFields(database, vals, self.type, self.fields)

class Milk:
    def __init__(self):
        self.type = "MilkInfo"
        self.fields = " (cowID, measure_time, station, volume)" \
                      " VALUES (%s, %s, %s, %s)"

    def convert(self, volumes, milk):
        volumes = numpy.array(volumes)
        milk = numpy.array(milk)
        volumeDict = dict(map(lambda x: (x[0]+'-'+x[1][:10], x[2]), volumes))
        for i in volumeDict:
            print(i)
        def volHandle(x):
            try:
                return volumeDict[x[0]+'-'+x[1][:10]]
            except:
                return 'NULL'
        vols = numpy.array(list(map(volHandle, milk)))
        milkWithVol = numpy.column_stack((milk, vols))
        return tuple(map(tuple, milkWithVol))