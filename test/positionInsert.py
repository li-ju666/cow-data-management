import mysql.connector
from pandas import read_csv
import numpy
import datetime


# Read data from CSV file
def readData(filename):
    data = read_csv(filename, sep=",")
    return numpy.array(data)


# Check if a certain position table exist:
# if not, create it
#
# Side effect: create new table in database
#
def checkPositionTable(tableName, database):
    cursor = database.cursor()
    statement = "CREATE TABLE IF NOT EXISTS "+tableName + \
                " (type VARCHAR(255), ID INT, time DATETIME PRIMARY KEY, data VARCHAR(255))"
    # print(statement)
    cursor.execute(statement)
    database.commit()
    cursor.close()


# Insert a record to table
#
# Side effect: insert a record to database
#
def insertRecord(tableName, database, dataType, sensorID, time, recordData):
    cursor = database.cursor()
    statement = "INSERT INTO "+tableName+" (type, ID, time, data) VALUES (%s, %s, %s, %s)"
    val = (dataType, sensorID, time, recordData)
    cursor.execute(statement, val)
    database.commit()
    cursor.close()


positiondb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="example",
    database="position"
)

path = "data/position/"
FA = readData(path+"FA_20200921T000000UTC.csv")

timeFormat = '%Y-%m-%d %H:%M:%S'
failed = []
for i in range(len(FA)):
    print("Now for ", i)
    dataType = FA[i, 0]
    sensorID = FA[i, 1]
    tableName = FA[i, 2]
    time = datetime.datetime.fromtimestamp(FA[i, 3] / 1000).strftime(timeFormat)
    recordData = str(FA[i, 4:])
    try:
        checkPositionTable(tableName, positiondb)
        insertRecord(tableName, positiondb, dataType, sensorID, time, recordData)
    except:
        print("Failed: ", i)
        failed.append(i)
positiondb.close()
