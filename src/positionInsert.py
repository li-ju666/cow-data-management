# import mysql.connector
# from pandas import read_csv
# import numpy
import time
from src.lib.typeclass import FA, PA, PAA, PC
from src.helper import insert
# from src.lib.dbinit import connect


# Read data from CSV file
# def readData(filename):
#     data = read_csv(filename, sep=",")
#     return numpy.array(data)

# def checkDatabase(dbName, database):
#     cursor = database.cursor()
#     statement = "CREATE DATABASE IF NOT EXISTS "+dbName
#     cursor.execute(statement)
#     database.commit()
#     cursor.close()
#
# # create new table:
# # Side effect: create new table in database
# #
# def checkPositionTables(database):
#     FAstatement = "CREATE TABLE IF NOT EXISTS FA " \
#                   "(tag_str VARCHAR(10), " \
#                   "measure_time TIMESTAMP(3), " \
#                   "posX SMALLINT UNSIGNED, " \
#                   "posY SMALLINT UNSIGNED, " \
#                   "posZ SMALLINT UNSIGNED, " \
#                   "PRIMARY KEY (tag_str, measure_time))"
#     PAstatement = "CREATE TABLE IF NOT EXISTS PA " \
#                   "(tag_str VARCHAR(10), " \
#                   "start_time TIMESTAMP(3), " \
#                   "end_time TIMESTAMP(3), " \
#                   "posX SMALLINT UNSIGNED, " \
#                   "posY SMALLINT UNSIGNED, " \
#                   "posZ SMALLINT UNSIGNED, " \
#                   "activity_type SMALLINT, " \
#                   "distance SMALLINT, " \
#                   "PRIMARY KEY (tag_str, start_time, end_time))"
#     PAAstatement ="CREATE TABLE IF NOT EXISTS PAA " \
#                   "(tag_str VARCHAR(10), " \
#                   "measure_time TIMESTAMP(3), " \
#                   "interv INT , " \
#                   "activity_type SMALLINT UNSIGNED, " \
#                   "distance SMALLINT UNSIGNED, " \
#                   "period SMALLINT UNSIGNED, " \
#                   "duration INT, " \
#                   "PRIMARY KEY (tag_str, measure_time, activity_type))"
#     PCstatement = "CREATE TABLE IF NOT EXISTS PC " \
#                   "(tag_str VARCHAR(10), " \
#                   "start_time TIMESTAMP(3), " \
#                   "end_time TIMESTAMP(3), " \
#                   "posX SMALLINT UNSIGNED, " \
#                   "posY SMALLINT UNSIGNED, " \
#                   "posZ SMALLINT UNSIGNED, " \
#                   "PRIMARY KEY (tag_str, start_time, end_time))"
#
#     statements = [FAstatement, PAstatement, PAAstatement, PCstatement]
#     for statement in statements:
#         # print(statement)
#         cursor = database.cursor()
#         cursor.execute(statement)
#         database.commit()
#         cursor.close()

#
# def connect():
#     db = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="example"
#     )
#
#     ## make sure database position exists: if not, create it
#     checkDatabase("position", db)
#
#     ## connect to position database
#     positiondb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="example",
#         database="position"
#     )
#     checkPositionTables(positiondb)
#     return positiondb

# positiondb = connect()
# checkPositionTables(positiondb)
#
#
#
# def insert(fileName, Insertor):
#     start = time.time()
#     ## data read
#     data = readData(fileName)
#
#     ## connect to sql server
#     positiondb = connect()
#     #
#     ## data preparation
#     insertor = Insertor()
#     tableName = insertor.type
#     vals = insertor.convert(data)
#     # return vals
#     ## data insertion
#     insertStart = time.time()
#     insertor.insert(positiondb, vals)
#     positiondb.close()
#
#     # time test
#     print("Total time: ", time.time()-start)
#     print("Insertion time: ", time.time()-insertStart)
# #
#
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