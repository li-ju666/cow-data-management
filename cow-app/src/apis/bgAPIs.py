import threading
from src.apis.scan_se import scan
from src.apis.query import positionQuery, infoQuery, directQuery


def bgScanSe():
    try:
        thread = threading.Thread(target=scan)
        thread.start()
        return "Swedish files scan started... "
    except:
        return "Failed to scan Swedish files"


def bgPosQuery(cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic):
    try:
        thread = threading.Thread(target=positionQuery,
                                  args = (cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic))
        thread.start()
        return "Querying... "
    except:
        return "Failed to start query"


def bgInfoQuery(cow_id, grp, stats, start_date, end_date, fields, type):
    try:
        thread = threading.Thread(target=infoQuery,
                                  args=(cow_id, grp, stats, start_date, end_date, fields, type))
        thread.start()
        return "Querying... "
    except:
        return "Failed to start query"

def bgDrctQuery(statement):
    try:
        thread = threading.Thread(target=directQuery, args=statement)
        thread.start()
        return "Querying... "
    except:
        return "Failed to start query"