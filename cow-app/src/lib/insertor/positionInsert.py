from src.lib.reader.positionReader import readPos
from .insertor import InsertorBase
import numpy
from src.lib.dbmanager.dbinit import connect_se, connect_nl

def insertPos(filePath, db):
    if db == "se":
        database = connect_se()
    else:
        database = connect_nl()
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

    step = 200000
    step_n = 0
    while True:
        data = readPos(filePath, nrows=step, skiprows=step_n*step)
        print(step_n, flush=True)
        insertor.insert(database, data)
        step_n += 1
        if data.shape[0] < step:
            break

    database.close()
    if db == "se":
        from src.lib.logmanager.logManage_se import saveLog
    else:
        from src.lib.logmanager.logManage_nl import saveLog
    saveLog(fileName)
    print("File inserted: {}".format(fileName), flush=True)


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
