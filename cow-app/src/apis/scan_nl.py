from src.lib.insertor.infoInsert_nl import insertMilk, insertMap
from src.lib.insertor.positionInsert import insertPos
from os import listdir, remove
from src.lib.logmanager.logManage_nl import readLog, saveLog
from src.lib.dbmanager.dbinit import connect_nl
import threading
import time

def infoScan(path):
    print("Scan for info files has started -----------------------------------------------------------", flush=True)
    db = connect_nl()
    files = listdir(path)

    CowFiles = list(filter((lambda x: x.startswith("Cow")), files))
    CowFiles.sort()

    MilkFiles = list(filter((lambda x: "control" in x), files))

    records = readLog()
    # print(records, flush=True)
    for file in MilkFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            insertMilk(path+file, db)
            saveLog(file)

    # print(KOFiles)
    for file in CowFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            insertMap(path+file, db)
            saveLog(file)
            remove(path+file)

    print("Info scan has completed", flush=True)
    db.close()


def positionScan(path):
    files = listdir(path)
    files.sort()
    # filter position files
    files = list(filter(
        lambda fname: fname.startswith("PA") or fname.startswith("FA") or fname.startswith("PC"), files))
    # select files which have not been inserted (i.e. not in log)
    records = readLog()
    files = list(filter(lambda x: x not in records, files))

    start = time.time()
    for file in files:
        # if file not in records:
        print("Inserting file: {}".format(file), flush=True)
        # insertPos(path+file, db)
        try:
            thread = threading.Thread(target=insertPos, args=[path+file, "nl"])
            thread.start()
            print("Position file inserting starts in new thread", flush=True)
#                return "Position file inserting starts in new thread"
        except:
            print("Failed to insert position file", flush=True)
        # saveLog(file)
    # print("Time cost: {}".format(time.time()-start), flush=True)
    # print("All position files have been submitted", flush=True)


def scan():
    path = "upload_files/nl/"
    infoScan(path)
    positionScan(path)
