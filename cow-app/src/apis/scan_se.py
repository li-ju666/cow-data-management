from src.lib.insertor.infoInsert_se import insertHealth, insertInfo, insertRef, insertMilkAV, insertMilkPlats
from src.lib.insertor.positionInsert import insertPos
from os import listdir
from src.lib.logmanager.logManage_se import readLog, saveLog
from src.lib.dbmanager.dbinit import connect_se
#from random import shuffle
#import multiprocessing, psutil, threading
import threading
import time

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
    # print(records, flush=True)
    for file in AvFiles:
        if file not in records:
            insertMilkAV(path+file, db)
            saveLog(file)

    for file in MilkFiles:
        if file not in records:
            insertMilkPlats(path+file, db)
            saveLog(file)

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
    # shuffle(files)

    # # decide how many threads to create, depending on number of cores and available memory
    # core_limit = multiprocessing.cpu_count()
    # print("Number of cpu: {}".format(core_limit), flush=True)
    # mem_limit = psutil.virtual_memory()[1]/1024/1024/1024/2
    # print("Memory limits: {}".format(mem_limit), flush=True)
    # file_limit = len(files)
    # num_threads = min([core_limit, mem_limit, file_limit])
    # print("Number of threads: {}".format(num_threads), flush=True)
    # tasks = []
    # num_per_thread = round(file_limit/num_threads)
    # for i in num_threads:
    #     tasks.append(files[i*num_per_thread:(i+1)*num_per_thread])
    #
    start = time.time()
    for file in files:
        # if file not in records:
        print("Inserting file: {}".format(file), flush=True)
        # insertPos(path+file, db)
        try:
            thread = threading.Thread(target=insertPos, args=[path+file, "se"])
            thread.start()
            print("Position file inserting starts in new thread", flush=True)
#                return "Position file inserting starts in new thread"
        except:
            print("Failed to insert position file", flush=True)
        # saveLog(file)
    # print("Time cost: {}".format(time.time()-start), flush=True)
    # print("All position files have been submitted", flush=True)


def scan():
    path = "upload_files/se/"
    infoScan(path)
    positionScan(path)
