from src.lib.insertor.infoInsert_se import insertHealth, insertInfo, insertRef, insertMilkAV, insertMilkPlats
from src.lib.insertor.positionInsert import insertPos
from os import listdir, rename
from src.lib.logmanager.logManage_se import readLog, saveLog
from src.lib.dbmanager.dbinit import connect_se
from re import findall
from random import shuffle
import psutil
import threading
import time

def infoScan(path):
    print("Scan for info files has started -----------------------------------------------------------", flush=True)
    db = connect_se()
    files = listdir(path)

    KOFiles = list(filter((lambda x: x.startswith("KO")), files))
    KOFiles.sort()

    rawHealthFiles = list(filter((lambda x: "versikt" in x), files))
    HealthFiles = []
    for file in rawHealthFiles:
        targetName = "Översikt " + findall("\d+", file)[-1] + ".txt"
        HealthFiles.append(targetName)
        rename(path+file, path+targetName)
    HealthFiles.sort()

    AvFiles = list(filter((lambda x: x.startswith("Avkastn")), files))
    AvFiles.sort()

    rawMilkFiles = list(filter((lambda x: "lkplats" in x), files))
    MilkFiles = []
    for file in rawMilkFiles:
        targetName = "Mjölkplats" + findall("\d+", file)[-1] + ".txt"
        MilkFiles.append(targetName)
        rename(path + file, path + targetName)
    MilkFiles.sort()

    records = readLog()
    # print(records, flush=True)
    for file in AvFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            try:
                insertMilkAV(path+file, db)
                saveLog(file)
            except:
                continue

    for file in MilkFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            try:
                insertMilkPlats(path+file, db)
                saveLog(file)
            except:
                continue
    # print(KOFiles)
    for file in KOFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            try:
                insertInfo(path+file, db)
                insertRef(path+file, db)
                saveLog(file)
            except:
                continue
    for file in HealthFiles:
        if file not in records:
            print("{} inserting. ".format(file), flush=True)
            try:
                insertHealth(path+file, db)
                saveLog(file)
            except:
                continue
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
    n_threads = min(psutil.cpu_count(), len(files), int(psutil.virtual_memory()[1]/(3*1024*1024*1024)))
    if len(files) != 0 and n_threads == 0:
        raise RuntimeError('No enough resources available: please try later')
    else:
        print("Number of threads: {}".format(n_threads), flush=True)
        tasks = [files[i::n_threads] for i in range(n_threads)]

        def thread_job(files):
            for file in files:
                try:
                    insertPos(file, "se")
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
    path = "upload_files/se/"
    infoScan(path)
    positionScan(path)
