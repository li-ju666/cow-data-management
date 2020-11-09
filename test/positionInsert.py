import mysql.connector
from pandas import read_csv
import numpy
import datetime
import time
from multiprocessing import Process, Manager, Pool


# Read data from CSV file
def readData(filename):
    data = read_csv(filename, sep=",")
    return numpy.array(data)

def checkDatabase(dbName, database):
    cursor = database.cursor()
    statement = "CREATE DATABASE IF NOT EXISTS "+dbName
    cursor.execute(statement)
    database.commit()
    cursor.close()


# Check if a certain position table exist:
# if not, create it
#
# Side effect: create new table in database
#


## FA: type, t1, px, py, pz
## PC: type, t1, t2, px, py, pz
## PA: type, t1, t2, px, py, pz, act, dis
# PAA: type, t1, interval, act, dis, period, dur
def checkPositionTable(tableName, database):
    cursor = database.cursor()
    statement = "CREATE TABLE IF NOT EXISTS "+tableName + \
                " (type VARCHAR(10), " \
                "time1 TIMESTAMP(3), " \
                "time2 TIMESTAMP(3), " \
                "posX INT, " \
                "posX INT, " \
                "posZ INT, " \
                "activity INT, " \
                "distance INT, " \
                "period INT, " \
                "duration INT" \
                "" \
                "PRIMARY KEY (time1, type))"
    print(statement)
    cursor.execute(statement)
    database.commit()
    cursor.close()


# Insert a record to table
#
# Side effect: insert a record to database
#
## FA: type, t1, px, py, pz
## PC: type, t1, t2, px, py, pz
## PA: type, t1, t2, px, py, pz, act, dis
# PAA: type, t1, interval, act, dis, period, dur

def insertPCRecord(tableName, database, val):
    cursor = database.cursor()
    statement = "INSERT INTO "+tableName+\
                " (type, time1, time2, posX, posY, posZ) VALUES (%s, %s, %s, %s, %s, %s)"
    cursor.executemany(statement, val)
    database.commit()
    cursor.close()

def insertPARecord(tableName, database, val):
    cursor = database.cursor()
    statement = "INSERT INTO "+tableName+\
                " (type, time1, time2, posX, posY, posZ, act, distance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(statement, val)
    database.commit()
    cursor.close()

def insertPAARecord(tableName, database, val):
    cursor = database.cursor()
    statement = "INSERT INTO "+tableName+\
                " (type, time1, interval, activity, distance, period, duration) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.executemany(statement, val)
    database.commit()
    cursor.close()

start = time.time()
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="example"
)

checkDatabase("position", db)
positiondb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="example",
    database="position"
)

path = "data/position/"
FA = readData(path+"FA_20200921T000000UTC.csv")

timeFormat = '%Y-%m-%d %H:%M:%S.%f'

tableNames = numpy.unique(FA[:, 2])
tableNames = list(map(lambda x: "`"+x+"`", tableNames))

for name in tableNames:
    checkPositionTable(name, positiondb)

# # for i in range(len(FA)):
#     if i%1000 == 0:
#         print("Now i is: ", i)
#     dataType = FA[i, 0]
#     sensorID = FA[i, 1]
#     tableName = "`"+FA[i, 2]+"`"
#     time = datetime.datetime.fromtimestamp(FA[i, 3]/1000.0).strftime(timeFormat)
#     recordData = str(FA[i, 4:])
#     insertRecord(tableName, positiondb, dataType, sensorID, time, recordData)

## =========================== slow but correct ===============================
# vals = {}
# count=0
# # to be optimized
# for i in FA:
#     count+=1
#     if count%100000 == 0:
#         print("Reformating...", count/len(FA)*100, "%")
#     tableName = "`"+i[2]+"`"
#     if vals.get(tableName) is None:
#         vals[tableName] = []
#     vals[tableName].append((i[0],
#                             datetime.datetime.fromtimestamp(i[3]/1000.0).strftime(timeFormat), str(i[4:])))
#     # if count == 100000:
#     #     break
## =========================== slow but correct ==============================

## =========================== to optimize ===================================
## 1. apply along axis
# def rowProcess(input):
#     result = ["`" + input[0] + "`",
#               input[1],
#               datetime.datetime.fromtimestamp(input[2]/1000.0).strftime(timeFormat),
#               "".join([str(elem) + "," for elem in input[3:]])]
#     return result
#
# reformated = numpy.column_stack((FA[:, 2], FA[:, 0], FA[:, 3], FA[:, 4:]))
# reformated = numpy.apply_along_axis(rowProcess, 1, reformated)
#
# vals = {}
# for name in tableNames:
#     print("preparing...", name)
#     mask = reformated[:, 0] == name
#     vals[name] = list(map(tuple, reformated[mask][:, 1:]))

## 2. vectorize
# def strProcess(input):
#     result = "".join([str(elem) + "," for elem in input])
#     return result
#
# nameVec = numpy.vectorize(lambda x: "`"+x+"`")
# dateTransVec = numpy.vectorize(lambda x: datetime.datetime.fromtimestamp(x/1000.0).strftime(timeFormat))
#
# strColumn = numpy.apply_along_axis(strProcess, 1, FA[:, 4:])
# reformated = numpy.column_stack(
#     (nameVec(FA[:, 2]), FA[:, 0], dateTransVec(FA[:, 3]), strColumn))
#
# vals = {}
# for name in tableNames:
#     print("preparing...", name)
#     mask = reformated[:, 0] == name
#     vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))

## 3. multiprocessing
manager = Manager()
results = manager.dict()
def strProcess(array, num, results):
     result = numpy.apply_along_axis(
        lambda x: "".join([str(elem) + "," for elem in x]), 1, array)
     results[num] = result

def nameVec(array, num, results):
    func = numpy.vectorize(lambda x: "`"+x+"`")
    results[num] = func(array)

def dateTransVec(array, num, results):
    func = numpy.vectorize(lambda x: datetime.datetime.fromtimestamp(x/1000.0).strftime(timeFormat))
    results[num] = func(array)

jobs = []
jobs.append(Process(target=nameVec, args=(FA[:, 2], 0, results)))
jobs.append(Process(target=dateTransVec, args=(FA[:, 3], 1, results)))
jobs.append(Process(target=strProcess, args=(FA[:, 4:], 2, results)))

for proc in jobs:
    proc.start()

for proc in jobs:
    proc.join()
# strColumn = numpy.apply_along_axis(strProcess, 1, FA[:, 4:])
# reformated = numpy.column_stack(
#     (nameVec(FA[:, 2]), FA[:, 0], dateTransVec(FA[:, 3]), strColumn))

reformated = numpy.column_stack((results[0],
                                 FA[:, 0], results[1], results[2]))

vals = {}
for name in tableNames:
    print("preparing...", name)
    mask = reformated[:, 0] == name
    vals[name] = tuple(map(tuple, reformated[mask][:, 1:]))

## ======================== try to optimize =================================


insertStart = time.time()
for i in vals:
    print("inserting...", i)
    insertPCRecord(i, positiondb, vals[i])

positiondb.close()
print("Total time: ", time.time()-start)
print("Insertion time: ", time.time()-insertStart)