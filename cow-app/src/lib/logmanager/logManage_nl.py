def saveLog(filename):
    with open("log/log_nl", "a") as f:
        f.write(filename+"\n")


def readLog():
    try:
        with open("log/log_nl", "r") as f:
            content = f.readlines()
        content = [x.strip() for x in content]
    except:
        content = []
    return content


def formatLog():
    records = readLog()
    return records
