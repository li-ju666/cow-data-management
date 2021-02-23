from src.lib.insertor.infoInsert_se import insertHealth, insertInfo, insertRef, insertMilk
from src.lib.insertor.positionInsert import insertPos
from os import listdir
from src.lib.logmanager.logManage_se import readLog, saveLog
from src.lib.dbmanager.dbinit import connect_se


def infoScan(path):
    db = connect_se()
    files = listdir(path)

    KOFiles = list(filter((lambda x: x.startswith("KO")), files))
    KOFiles.sort()

    HealthFiles = list(filter((lambda x: x.startswith("Översikt")), files))
    HealthFiles.sort()

    AvFiles = list(filter((lambda x: x.startswith("Avkastn")), files))
    AvFiles.sort()

    MilkFiles = list(filter((lambda x: x.startswith("Mjölkplats")), files))
    MilkFiles.sort()

    records = readLog()
    print(records, flush=True)
    # TODO: milk data insertion is not finished
    # for i in range(len(AvFiles)):
    #     insertMilk(path+AvFiles[i], path+MilkFiles[i])
    print(KOFiles)
    for file in KOFiles:
        if file not in records:
            insertInfo(path+file, db)
            insertRef(path+file, db)
            saveLog(file)

    for file in HealthFiles:
        if file not in records:
            insertHealth(path+file, db)
            saveLog(file)
    print("Info scan has completed")
    db.close()


def positionScan(path):
    db = connect_se()
    files = listdir(path)
    files.sort()
    records = readLog()

    for file in files:
        if file not in records:
            print("Inserting file: {}".format(file), flush=True)
            insertPos(path+file, db)
            saveLog(file)
    print("Position scan has completed")
    db.close()


def scan():
    path = "upload_files/se/"
    infoScan(path)
    positionScan(path)