from abc import ABC, abstractmethod
import numpy
import datetime


class InsertorBase(ABC):
    # abstract insertor class definition
    def __init__(self):
        """"""

    @abstractmethod
    def convert(self, data):
        pass

    @abstractmethod
    def insert(self, database, data):
        pass

    @staticmethod
    def insertWithFields(database, vals, type, fields):
        # maxLen = len(vals)
        # startIdx = 0
        # endIdx = 0
        # step = 200000
        cursor = database.cursor()
        # while endIdx < maxLen:
        #     print("All records: ", startIdx, "/", maxLen, "  Percentage: ", round(startIdx / maxLen * 100, 2), "%",
        #           flush=True)
        #     if startIdx + step > maxLen:
        #         endIdx = maxLen
        #     else:
        #         endIdx += step
        #     print(startIdx, endIdx)
        #     # cursor = database.cursor()
        #     statement = "INSERT INTO " + type + fields
        #     cursor.executemany(statement, vals[startIdx:endIdx])
        #     # database.commit()
        #     # cursor.close()
        #     startIdx = endIdx
        statement = "INSERT INTO " + type + fields
        cursor.executemany(statement, vals)
        cursor.close()
        database.commit()

    @staticmethod
    def dateVec(time):
        def timeConvert(time):
            timeFormat = '%Y-%m-%d %H:%M:%S.%f'
            return datetime.datetime.fromtimestamp(time / 1000.0).strftime(timeFormat)
        return numpy.vectorize(timeConvert)(time)