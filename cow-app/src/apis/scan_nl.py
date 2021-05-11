from src.lib.insertor.infoInsert_nl import insertMilk, insertMap
from src.lib.insertor.positionInsert import insertPos
from os import listdir, remove
from src.lib.logmanager.logManage_nl import readLog, saveLog
from src.lib.dbmanager.dbinit import connect_nl
import threading
from random import shuffle
import psutil

def infoScan(path):
    print("Scan for info files has started -----------------------------------------------------------", flush=True)
    db = connect_nl()
    files = listdir(path)

    CowFiles = list(filter((lambda x: x.startswith("Cow")), files))
    CowFiles.sort()
    CowFiles = []

    MilkFiles = list(filter((lambda x: "control" in x), files))

    records = readLog()
    MilkFiles = list(filter(lambda file: file not in records, MilkFiles))
    # print(records, flush=True)
    for file in MilkFiles:
        print("{} inserting. ".format(file), flush=True)
        try:
            insertMilk(path+file, db)
            saveLog(file)
        except:
            continue
    # print(KOFiles)
    # for file in CowFiles:
    #     if file not in records:
    #         print("{} inserting. ".format(file), flush=True)
    #         insertMap(path+file, db)
    #         saveLog(file)
    #         remove(path+file)

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
    files = list(map(lambda file: path+file, files))
    shuffle(files)
    n_threads = min(psutil.cpu_count(), len(files), int(psutil.virtual_memory()[1]/(1.5*1024*1024*1024)))
    print("Number of cpu: {}".format(n_threads), flush=True)
    tasks = [files[i::n_threads] for i in range(n_threads)]

    def thread_job(files):
        for file in files:
            try:
                insertPos(file, "nl")
            except Exception as e:
                print(e, flush=True)
                continue

    for i in range(n_threads):
        try:
            thread = threading.Thread(target=thread_job, args=[tasks[i]])
            thread.start()
            print("Position file inserting starts in new thread", flush=True)
        except Exception as e:
            print(e, flush=True)
            continue


def scan():
    path = "upload_files/nl/"
    infoScan(path)
    positionScan(path)
