from src.backend.lib.typeclass import FA, PA, PAA, PC
from src.backend.lib.positionInsert import insertpos
from os import listdir
from src.backend.lib.logManage import readLog, saveLog


def positionScan():
    path = "input_files/position/"

    files = listdir(path)

    FAFiles = list(filter((lambda x: x.startswith("FA")), files))
    FAFiles.sort()

    PAFiles = list(filter((lambda x: x.startswith("PA")), files))
    PAAFiles = list(filter((lambda x: x.startswith("PAA")), files))
    PAAFiles.sort()
    PAFiles = [x for x in PAFiles if x not in PAAFiles]
    PAFiles.sort()

    PCFiles = list(filter((lambda x: x.startswith("PC")), files))
    PCFiles.sort()

    records = readLog()

    for file in FAFiles:
        if file not in records:
            insertpos(path+file, FA)
            saveLog(file)

    for file in PAFiles:
        if file not in records:
            insertpos(path+file, PA)
            saveLog(file)

    for file in PAAFiles:
        if file not in records:
            insertpos(path+file, PAA)
            saveLog(file)

    for file in PCFiles:
        if file not in records:
            insertpos(path+file, PC)
            saveLog(file)
    print("Position scan has completed")
