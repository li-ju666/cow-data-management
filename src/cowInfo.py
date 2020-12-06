from src.lib.dbinit import connect
from src.lib.read import readKO, readHealth
from src.lib.typeclass import KO, Health
from re import findall

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
    for i in data:
        print(i)
    ## data preparation
    health = Health()
    insertDate = findall("\d+", fileName)[0]
    data = health.convert(data, insertDate)

    ## data insertion
    health.insert(db, data)
    db.close()