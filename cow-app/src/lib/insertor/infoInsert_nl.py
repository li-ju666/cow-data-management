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
        self.fields = " (diernr, ISO, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s, %s)"

    def convert(self, data):
        # TODO: implement the algorithm
        diernrs, ISO, tagStr, startDates, endDates = [], [], [], [], []
        today = datetime.datetime.now().strftime("%y-%m-%d")
        for rec in data:
            rec_diernr, rec_iso, rec_tag, rec_start, comment = tuple(rec)
            if rec_diernr not in diernrs:
                diernrs.append(rec_diernr)
                ISO.append(rec_iso)
                tagStr.append(rec_tag)
                startDates.append(rec_start)
                endDates.append(today)
            else:
                # find all occurance of this cow
                indices = [i for i, x in enumerate(diernrs) if x == rec_diernr]
                # update latest change
                idx = indices[-1]
                endDates[idx] = rec_start
                # insert new tag record
                diernrs.append(rec_diernr)
                ISO.append(rec_iso)
                tagStr.append(rec_tag)
                startDates.append(rec_start)
                endDates.append(today)
        result = []
        for i in range(len(diernrs)):
            result.append((diernrs[i], ISO[i], tagStr[i], startDates[i], endDates[i]))
        return tuple(result)

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)
