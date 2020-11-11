import mysql.connector
from pandas import read_csv, unique
import numpy
import time
from src.lib.typeclass import FA, PA, PAA, PC


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

# create new table:
# Side effect: create new table in database
#
def checkPositionTable(tableName, database):
    cursor = database.cursor()
    statement = "CREATE TABLE IF NOT EXISTS "+tableName + \
                " (type VARCHAR(10), " \
                "time1 TIMESTAMP(3), " \
                "time2 TIMESTAMP(3), " \
                "posX SMALLINT UNSIGNED, " \
                "posY SMALLINT UNSIGNED, " \
                "posZ SMALLINT UNSIGNED, " \
                "intv INT UNSIGNED, " \
                "act SMALLINT UNSIGNED, " \
                "dist SMALLINT UNSIGNED, " \
                "per SMALLINT UNSIGNED, " \
                "dur INT UNSIGNED, " \
                "PRIMARY KEY (time1, type))"
    # print(statement)
    cursor.execute(statement)
    database.commit()
    cursor.close()

def checkAndInsertTable(tableNames, database):
    cursor = database.cursor()
    cursor.execute("SHOW TABLES")
    existingTables = cursor.fetchall()
    existingTables = ["`"+table[0][0]+"`" for table in existingTables]
    toBeCreated = list(set(tableNames).difference(set(existingTables)))
    print("Tables to be created...")
    print(toBeCreated)
    for tableName in toBeCreated:
        checkPositionTable(tableName, database)

def connect():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example"
    )

    ## make sure database position exists: if not, create it
    checkDatabase("position", db)

    ## connect to position database
    positiondb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="example",
        database="position"
    )
    return positiondb

def getTableNames(data):
    tableNames = unique(data[:, 2])
    return list(map(lambda x: "`" + x + "`", tableNames))

# def insertFA(fileName):
#     start = time.time()
#     ## data read
#     path = "data/position/"
#     data = readData(path+fileName)
#     tableNames = getTableNames(data)
#
#     ## connect to sql server
#     positiondb = connect()
#
#     ## table check
#     checkAndInsertTable(tableNames, positiondb)
#
#     ## data preparation
#     fa = FA()
#     vals = fa.convert(data, tableNames)
#
#     ## data insertion
#     insertStart = time.time()
#     fa.insert(positiondb, vals)
#     positiondb.close()
#
#     ## time test
#     print("Total time: ", time.time()-start)
#     print("Insertion time: ", time.time()-insertStart)
#
# def insertPA(fileName):
#     start = time.time()
#     ## data read
#     path = "data/position/"
#     data = readData(path+fileName)
#     tableNames = getTableNames(data)
#
#     ## connect to sql server
#     positiondb = connect()
#
#     ## table check
#     checkAndInsertTable(tableNames, positiondb)
#
#     ## data preparation
#     pa = PA()
#     vals = pa.convert(data, tableNames)
#     # return vals
#     ## data insertion
#     insertStart = time.time()
#     pa.insert(positiondb, vals)
#     positiondb.close()
#
#     ## time test
#     print("Total time: ", time.time()-start)
#     print("Insertion time: ", time.time()-insertStart)

def insert(fileName, Insertor):
    start = time.time()
    ## data read
    data = readData(fileName)
    tableNames = getTableNames(data)

    ## connect to sql server
    positiondb = connect()

    ## table check
    checkAndInsertTable(tableNames, positiondb)

    ## data preparation
    insertor = Insertor()
    vals = insertor.convert(data, tableNames)
    # return vals
    ## data insertion
    insertStart = time.time()
    insertor.insert(positiondb, vals)
    positiondb.close()

    ## time test
    print("Total time: ", time.time()-start)
    print("Insertion time: ", time.time()-insertStart)


start = time.time()
path = "data/position/"
f1 = "FA_20200921T000000UTC.csv"
f2 = "PA_20200921T000000UTC.csv"
f3 = "PAA_20200921T000000UTC.csv"
f4 = "PC_20200921T000000UTC.csv"
insert(path+f1, FA)
insert(path+f2, PA)
insert(path+f3, PAA)
insert(path+f4, PC)
print("overall time: ", time.time() - start)
# insertFA("FA_20200921T000000UTC.csv")
#vals = insertPA("PA_20200921T000000UTC.csv")