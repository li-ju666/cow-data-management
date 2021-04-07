from src.lib.reader.infoReader_nl import readCowData, readMilkData
from re import findall
import datetime
from .insertor import InsertorBase
import numpy


def insertMilk(fileName, db):
    # data read
    milkData = readMilkData(fileName)
    milk = CowMilk()
    nums = findall("\d+", fileName)
    insertDate = nums[0] + nums[1] + nums[2]
    # data insertion
    milk.insert(db, (milkData, insertDate))


def insertMap(fileName, db):
    data = readCowData(fileName)
    # data preparation
    cowmap = CowMap()

    # data insertion
    cowmap.insert(db, data)


"""" Insertor definitions for info tables for Swedish data """

class CowMilk(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "MilkInfo"
        cols = ' (diernr, insertdate, naam, levnr, kgmelk, ' \
            'isk, percentv, eiw, lact, ur, celget, klfdat, lftafk, mprlft, ' \
            'lactnr, lactatiedagen, kgmelklact, kgmelk305, vetlact, vet305, ' \
            'eiwlact, eiw305, kgvetlact, kgvet305, kgeiwlact, kgeiw305, lw)'
        self.fields = cols + " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, " \
                             "%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        data, insertDate = data
        fileDate = datetime.datetime.strptime(insertDate, "%Y%m%d")
        fileDate = fileDate.strftime("%y-%m-%d")
        data = tuple(map(lambda x: [x[0]] + [fileDate] + x[1:], data))
        return data

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class CowMap(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "Mapping"
        self.fields = " (diernr, tagStr, ISO, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s, %s)"

    def convert(self, data):
        # TODO: implement the algorithm
        # today = datetime.datetime.now()
        # refs = {}
        # for rec in data:

        return
        # today = datetime.datetime.now()
        #
        # return tuple(result)

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)