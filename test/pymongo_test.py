from pprint import pprint
from pymongo import MongoClient
from pandas import read_csv
import numpy
import datetime
import time as tm

# Connect to local mangodb "test" in table "pos_data"
client = MongoClient('localhost', port=27017)
db = client["mongoTest"]        #Database
#collection = db["records"]       #Collection

# Read data from CSV file
def readData(filename):
    #data = read_csv(filename, sep=",", nrows=100000)
    data = read_csv(filename, sep=",")
    return numpy.array(data)

def insertRecord(tagID, database, dataType, sensorID, time, recordData):
    #collection = database.tagID
    record_input = {
        'type':dataType,
        'ID':sensorID,
        'time':time,
        'data':recordData
    }
    #result = collection.insert_one(record_input)
    TagCollection = database[str(tagID)]
    result = TagCollection.insert_one(record_input)
    


#Loading pos. data from file
path = "data/position/"
FA = readData(path+"FA_20200921T000000UTC.csv")
pprint(str(len(FA)) + " entries read.")

timeFormat = '%Y-%m-%d %H:%M:%S'
failed = []

"""
# Approach 1, inserting each record one by one, 
# creating collections for each new tag
startTime = tm.time()
for i in range(len(FA)):
    if (i % 1000 == 0): 
        print("Iteration ",i)
    dataType = FA[i, 0]
    sensorID = FA[i, 1]
    tagID = FA[i, 2]
    time = datetime.datetime.fromtimestamp(FA[i, 3] / 1000).strftime(timeFormat)
    recordData = str(FA[i, 4:])

    try:
        #checkPositionTable(tableName, positiondb)
        insertRecord(tagID, db, dataType, sensorID, time, recordData)
    except:
        print("Failed: ", i)
        failed.append(i)
elapsed = tm.time() - startTime
pprint(str(len(FA)) + " entries uploaded in " + str(elapsed) + ".")

QueryTestCollection = db["0024E209"]
QueryResult = QueryTestCollection.find_one({"type":"FA"})
pprint(QueryResult)

"""

#Approach 2, sorting list before upload:
tagListOrder = []
tagListData = []
startTime = tm.time()
print("Splitting into lists corr. to tagID...")
for i in range(len(FA)):
    tagID = FA[i, 2]
    record_input = {
        'type':FA[i, 0],
        'ID':FA[i, 1],
        'time':datetime.datetime.fromtimestamp(FA[i, 3] / 1000).strftime(timeFormat),
        'data':str(FA[i, 4:])
    }
    if (tagID not in tagListOrder):
        tagListOrder.append(tagID)
        tagListData.append([record_input])
    else:
        index = tagListOrder.index(tagID)
        tagListData[index].append((record_input))
print("Done splitting. " + str(len(tagListOrder)) + " splits in " + str(tm.time() - startTime))
print("Uploading to database...")
# Now to uppload the sorted split lists to the db
startTime = tm.time()
for i in range(len(tagListOrder)):
    collection = db[str(tagListOrder[i])]
    try:
        result = collection.insert_many(tagListData[i])
    except:
        print("Failed: ", i)
        failed.append(i)
print("Uploaded " + str(len(FA)) + " records in " + str(tm.time()-startTime) + "s.")
#QueryTestCollection = db["0024E209"]
#QueryResult = QueryTestCollection.find_one({"time":"2020-09-21 02:00:15"})
#pprint(QueryResult)