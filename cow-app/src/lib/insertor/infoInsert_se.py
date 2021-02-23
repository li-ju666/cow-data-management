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


def insertMilk(fileNames, db):
    ## Arguments: insertMilk(("Avfile", "mjolkfile"), db)
    file1, file2 = fileNames
    f1 = readAvkastfile(file1)
    f2 = readMjolkplatsfile(file2)
    milk = Milk()
    milk.insert(db, (f1, f2))


def insertRef(fileName, db):
    kolista, dried = readKO(fileName)
    insertDate = findall("\d+", fileName)[0]
    driedOffDict = dict(zip(list(dried[0]), list(dried[4])))
    for i in kolista:
        # select all references binded to the cow
        statement = "SELECT * FROM Reference WHERE cowID = " + i[0] + " ORDER BY startDate"
        cur = db.cursor()
        cur.execute(statement)
        results = cur.fetchall()

        # if result list is empty: add record
        if len(results) == 0 and i[2] != 'NULL':
            statement = "INSERT INTO Reference (cowID, tagStr, startDate, endDate)" \
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
            statement = "UPDATE Reference SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
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
            statement = "UPDATE Reference SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
                        "' AND tagStr='" + results[-1][1] + "'"
            # print(statement)
            cur.execute(statement)
            db.commit()
            cur.close()
            cur = db.cursor()
            # Insert new record
            statement = "INSERT INTO Reference (cowID, tagStr, startDate, endDate)" \
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
        self.fields = " (cowID, measure_time, station, volume)" \
                      " VALUES (%s, %s, %s, %s)"

    def convert(self, data):
        volumes, milk = data
        volumes = numpy.array(volumes)
        milk = numpy.array(milk)
        volumeDict = dict(map(lambda x: (x[0]+'-'+x[1][:10], x[2]), volumes))

        def volHandle(x):
            try:
                return volumeDict[x[0]+'-'+x[1][:10]]
            except:
                return 'NULL'
        vols = numpy.array(list(map(volHandle, milk)))
        milkWithVol = numpy.column_stack((milk, vols))
        def handleMilkWithVol(x):
            x = list(x)
            return tuple(None if v == 'NULL' else v for v in x)
        return tuple(map(handleMilkWithVol, milkWithVol))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class Reference(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "Reference"
        self.fields = " (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"

    def convert(self, data):
        return data

    def insert(self, database, vals):
        self.insertWithFields(database, vals, self.type, self.fields)