from src.lib.dbinit import connect
from src.lib.read import readKO, readHealth, readMjolkplatsfile, readAvkastfile
from src.lib.typeclass import KO, Health, Milk
from re import findall
import datetime
from os import listdir


def insertInfo(fileName):
    ## data read
    kolista, dried = readKO(fileName)

    ## connect to sql server
    db = connect()

    ## data preparation
    ko = KO()
    insertDate = findall("\d+", fileName)[0]
    kolista, dried = ko.convert(kolista, dried, insertDate)
    # for i in dried:
    #     print(i)

    ## data insertion
    ko.insert(db, kolista, dried)
    db.close()

def insertHealth(fileName):
    data = readHealth(fileName)
    ## connect to sql server
    db = connect()
    ## data preparation
    health = Health()
    insertDate = findall("\d+", fileName)[0]
    data = health.convert(data, insertDate)

    ## data insertion
    health.insert(db, data)
    db.close()

def insertMilk(file1, file2):
    f1 = readAvkastfile(file1)
    f2 = readMjolkplatsfile(file2)
    # db = connect()
    # for i in f1:
    #     print(i)
    milk = Milk()
    data = milk.convert(f1, f2)
    for i in data:
        print(i)

def insertRef(kofile):
    kolista, dried = readKO(kofile)
    insertDate = findall("\d+", kofile)[0]
    db = connect()
    driedOffDict = dict(zip(list(dried[0]), list(dried[4])))
    for i in kolista:
        # select all references binded to the cow
        statement = "SELECT * FROM Reference WHERE cowID = " + i[0] + " ORDER BY startDate"
        cur = db.cursor()
        cur.execute(statement)
        results = cur.fetchall()

        # if result list is empty: add record
        if len(results) == 0 and i[2] != 'NULL':
            statement = "INSERT INTO Reference (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"
            # print(i[2])
            calvnDate = datetime.datetime.strptime(i[6], "%d-%m-%y")
            calvnDate = calvnDate.strftime("%y-%m-%d")
            cur.execute(statement, (i[0], i[2], calvnDate, None))
            db.commit()
            cur.close()
        # if no previous records exist + no tag carried on the cow, continue
        elif len(results) == 0 and i[2] == 'NULL':
            continue
        # if previous record is the same as current tag, continue
        elif results[-1][1] == i[2]:
            continue
        # if tag is not carried anymore, update records
        elif i[2] == 'NULL':
            # print("Tag removed")
            # print(i[2])
            # print(results)
            ######### dried off date as end date (???????????????????????????
            try:
                driedOffDate = datetime.datetime.strptime(driedOffDict[i[0]], "%d-%m-%y")
            except:
                driedOffDate = datetime.datetime.strptime(insertDate, "%y%m%d")
            driedOffDate = driedOffDate.strftime("%y-%m-%d")
            statement = "UPDATE Reference SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
                        "' AND tagStr='" + results[-1][1] + "'"
            cur.execute(statement)
            db.commit()
            cur.close()
        else:
            # Update previous record
            print("Unexpected remove")
            print(i[2])
            print(results)
            try:
                driedOffDate = datetime.datetime.strptime(driedOffDict[i[0]], "%d-%m-%y")
            except:
                driedOffDate = datetime.datetime.strptime(insertDate, "%y%m%d")
            driedOffDate = driedOffDate.strftime("%y-%m-%d")
            statement = "UPDATE Reference SET endDate='" + driedOffDate + "' WHERE cowID='" + i[0] + \
                        "' AND tagStr='" + results[-1][1] + "'"
            print(statement)
            cur.execute(statement)
            db.commit()
            cur.close()
            cur = db.cursor()
            # Insert new record
            statement = "INSERT INTO Reference (cowID, tagStr, startDate, endDate)" \
                      " VALUES (%s, %s, %s, %s)"
            cur.execute(statement, (i[0], i[2], driedOffDate, None))
            db.commit()
            cur.close()
        # print(statement)
#
# # insertMilk("data/info/Avkastn 14 dag 201012.txt", "data/info/Mjölkplats 201012.txt")
# # data = readMjolkplatsfile("data/info/Mjölkplats 201026.txt")
# insertRef("data/info/KO info 201006.txt")
# newValues = len(list(filter(lambda x: x[2] != 'NULL', ko)))