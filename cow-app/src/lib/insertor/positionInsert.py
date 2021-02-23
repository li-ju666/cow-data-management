from src.lib.reader.positionReader import readPos
from .insertor import InsertorBase
import numpy


def insertPos(filePath, database):
    fileName = filePath[filePath.rfind("/")+1:]
    if fileName.startswith("PAA"):
        insertor = PAA()
    elif fileName.startswith("PA"):
        insertor = PA()
    elif fileName.startswith("FA"):
        insertor = FA()
    elif fileName.startswith("PC"):
        insertor = PC()
    else:
        print("Skipped", flush=True)
        return

    data = readPos(filePath)

    insertor.insert(database, data)


""" Position insertor definitions """


class FA(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "FA"
        self.fields = " (tag_id, tag_str, measure_time, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        reformated = numpy.column_stack((data[:, 1:3], self.dateVec(data[:, 3]), data[:, 4:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class PA(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "PA"
        self.fields = " (tag_id, tag_str, start_time, end_time, posX, posY, posZ, activity_type, distance)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        reformated = numpy.column_stack((data[:, 1:3], self.dateVec(data[:, 3]), self.dateVec(data[:, 4]), data[:, 5:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class PAA(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "PAA"
        self.fields = " (tag_id, tag_str, measure_time, interv, activity_type, distance, period, duration)" \
                      " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data")
        # reformated = (nameVec(data[:, 2]), data[:, 0], dateVec(data[:, 3]), data[:, 4:])
        reformated = numpy.column_stack((data[:, 1:3], self.dateVec(data[:, 3]), data[:, 4:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)


class PC(InsertorBase):
    def __init__(self):
        super().__init__()
        self.type = "PC"
        self.fields = " (tag_id, tag_str, start_time, end_time, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    def convert(self, data):
        print("Converting data", flush=True)
        reformated = numpy.column_stack((data[:, 1:3], self.dateVec(data[:, 3]), self.dateVec(data[:, 4]), data[:, 5:]))
        return tuple(map(tuple, reformated))

    def insert(self, database, data):
        vals = self.convert(data)
        self.insertWithFields(database, vals, self.type, self.fields)
