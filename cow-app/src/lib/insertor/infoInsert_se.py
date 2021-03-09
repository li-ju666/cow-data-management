from src.lib.reader.infoReader_se import readKO, readHealth, readMjolkplatsfile, readAvkastfile
from re import findall
import datetime
from .insertor import InsertorBase
import numpy


def insertInfo(fileName, db):
    # data read
    kolista, dried = readKO(fileName)
    ko = KO()
    insertDate = findall("\d+", fileName)[0]

    # data insertion
    ko.insert(db, (kolista, dried, insertDate))


def insertHealth(fileName, db):
    data = readHealth(fileName)
    # data preparation
    health = Health()
    insertDate = findall("\d+", fileName)[0]

    # data insertion
    health.insert(db, (data, insertDate))


def insertMilkAV(fileName, db):
    data = readAvkastfile(fileName)
    milkav = Milk()
    insertDate = findall("\d+", fileName)[1]
    milkav.insert(db, (data, insertDate))


def insertMilkPlats(fileName, db):
    data = readMjolkplatsfile(fileName)
    milkplat = Milk()
    insertDate = findall("\d+", fileName)[0]
    milkplat.insert(db, (data, insertDate))


def insertRef(fileName, db):
    kolista, dried = readKO(fileName)
    insertDate = findall("\d+", fileName)[0]
    driedOffDict = dict(zip(list(dried[0]), list(dried[4])))
    for i in kolista:
        # select all references binded to the cow
        statement = "SELECT * FROM Mapping WHERE cowID = " + i[0] + " ORDER BY startDate"
        cur = db.cursor()
        cur.execute(statement)
        results = cur.fetchall()

        # if result list is empty: add record
        if len(results) == 0 and i[2] != 'NULL':
            statement = "INSERT INTO Mapping (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"
            calvnDate = datetime.datetime.strptime(i[6], "%d-%m-%y")
            calvnDate = calvnDate.strftime("%y-%m-%d")
            cur.execute(statement, (i[0], i[2], calvnDate, None))
            db.commit()
            cur.close()
        # if no previous records exist + no tag carried on the cow, continue
        elif len(results) == 0 and i[2] == 'NULL':
            continue
        # if previous record is the same as current tag, continue
        elif results[-1][1] == i[2]:
            continue
        # if tag is not carried anymore, update records
        elif i[2] == 'NULL':
            ######### dried off date as end date (???????????????????????????
            try:
                driedOffDate = datetime.datetime.strptime(driedOffDict[i[0]], "%d-%m-%y")
            except:
                driedOffDate = datetime.datetime.strptime(insertDate, "%y%m%d")
            driedOffDate = driedOffDate.strftime("%y-%m-%d")
            statement = "UPDATE Mapping SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
                        "' AND tagStr='" + results[-1][1] + "'"
            cur.execute(statement)
            db.commit()
            cur.close()
        else:
            # Update previous record
            # print("Unexpected remove")
            # print(i[2])
            # print(results)
            try:
                driedOffDate = datetime.datetime.strptime(driedOffDict[i[0]], "%d-%m-%y")
            except:
                driedOffDate = datetime.datetime.strptime(insertDate, "%y%m%d")
            driedOffDate = driedOffDate.strftime("%y-%m-%d")
            statement = "UPDATE Mapping SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
                        "' AND tagStr='" + results[-1][1] + "'"
            # print(statement)
            cur.execute(statement)
            db.commit()
            cur.close()
            cur = db.cursor()
            # Insert new record
            statement = "INSERT INTO Mapping (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"
            cur.execute(statement, (i[0], i[2], driedOffDate, None))
            db.commit()
            cur.close()


"""" Insertor definitions for info tables for Swedish data """


class KO(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type1 = "CowInfo"
        self.fields1 = " (cowID, insertDate, resp, grp, stat, lakt, kalvn_date) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        self.type2 = "InsemInfo"
        self.fields2 = " (cowID, insertDate, gp, avsinad, insem_date, sedan_insem, insem_tjur, forv_kalvn, " \
                       "tid_ins, tid_mellan) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        """Input: (kolista, dried, insertDate)"""
        kolista, dried, insertDate = data
        print("Converting data", flush=True)
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

        def removeNull(x):
            return tuple(map(lambda x: None if x == 'NULL' else x, x))
        return tuple(map(removeNull, kolista)), tuple(map(removeNull, dried))

    def insert(self, database, data):
        kolista, dried = self.convert(data)
        self.insertWithFields(database, kolista, self.type1, self.fields1)
        self.insertWithFields(database, dried, self.type2, self.fields2)


class Health(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "HealthInfo"
        self.fields = " (cowID, insertDate, 7dag, 100dag, handelse_day, comments)" \
                      " VALUES (%s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        data, insertDate = data
        print("Converting data", flush=True)
        # print(data[0,4])
        # print(data[0,5])
        fileDate = datetime.datetime.strptime(insertDate, "%y%m%d")
        fileDate = fileDate.strftime("%y-%m-%d")
        reformated = numpy.column_stack((data[:, 0], numpy.repeat(fileDate, len(data)),
                                         data[:, -4:]))

        def removeNull(x):
            x = tuple(map(lambda x: None if x == 'NULL' else x, x))
            return x[:-1] + (x[-1].replace("\n", "").replace('"', ''), )
        return tuple(map(removeNull, reformated))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class Milk(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "MilkInfo"
        self.fields = " (cowID, insertDate, recordType, record)" \
                      " VALUES (%s, %s, %s, %s)"

    def convert(self, data):
        data, insertDate = data
        fileDate = datetime.datetime.strptime(insertDate, "%y%m%d")
        fileDate = fileDate.strftime("%y-%m-%d")

        def volHandle(x):
            return x[0], fileDate, x[1], x[2]

        return tuple(map(volHandle, data))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class Mapping(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "Mapping"
        self.fields = " (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"

    def convert(self, data):
        return data

    def insert(self, database, vals):
        self.insertWithFields(database, vals, self.type, self.fields)