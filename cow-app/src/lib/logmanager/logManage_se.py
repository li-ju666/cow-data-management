def saveLog(filename):
    with open("log/log_se", "a") as f:
        f.write(filename+"\n")


def readLog():
    try:
        with open("log/log_se", "r") as f:
            content = f.readlines()
        content = [x.strip() for x in content]
    except:
        content = []
    return content


def formatLog():
    records = readLog()
    KOFiles = list(filter((lambda x: x.startswith("KO")), records))
    KOFiles.sort()

    HealthFiles = list(filter((lambda x: x.startswith("Översikt")), records))
    HealthFiles.sort()

    AvFiles = list(filter((lambda x: x.startswith("Avkastn")), records))
    AvFiles.sort()

    MilkFiles = list(filter((lambda x: x.startswith("Mjölkplats")), records))
    MilkFiles.sort()

    FAFiles = list(filter((lambda x: x.startswith("FA")), records))
    FAFiles.sort()

    PAFiles = list(filter((lambda x: x.startswith("PA")), records))
    PAAFiles = list(filter((lambda x: x.startswith("PAA")), records))
    PAAFiles.sort()
    PAFiles = [x for x in PAFiles if x not in PAAFiles]
    PAFiles.sort()

    PCFiles = list(filter((lambda x: x.startswith("PC")), records))
    PCFiles.sort()

    records = dict()
    records["KO"] = KOFiles
    records["Health"] = HealthFiles
    records["Avkastn"] = AvFiles
    records["Milk"] = MilkFiles
    records["FA"] = FAFiles
    records["PA"] = PAFiles
    records["PAA"] = PAAFiles
    records["PC"] = PCFiles
    return records
