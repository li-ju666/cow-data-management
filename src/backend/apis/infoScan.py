from src.backend.lib.infoInsert import insertHealth, insertInfo, insertRef, insertMilk
from os import listdir
from src.backend.lib.logManage import readLog, saveLog

def infoScan():
    path = "input_files/info/"
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

    # TODO: milk data insertion is not finished
    # for i in range(len(AvFiles)):
    #     insertMilk(path+AvFiles[i], path+MilkFiles[i])
    print(KOFiles)
    for file in KOFiles:
        if file not in records:
            insertInfo(path+file)
            insertRef(path+file)
            saveLog(file)

    for file in HealthFiles:
        if file not in records:
            insertHealth(path+file)
            saveLog(file)
    print("Info scan has completed")