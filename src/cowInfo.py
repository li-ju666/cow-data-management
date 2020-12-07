from src.lib.dbinit import connect
from src.lib.read import readKO, readHealth, readMjolkplatsfile, readAvkastfile
from src.lib.typeclass import KO, Health, Milk
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

# insertMilk("data/info/Avkastn 14 dag 201012.txt", "data/info/Mjölkplats 201012.txt")
# # data = readMjolkplatsfile("data/info/Mjölkplats 201026.txt")