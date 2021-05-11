import threading

def bgScanSe():
    from src.apis.scan_se import scan
    # try:
    #     thread = threading.Thread(target=scan)
    #     thread.start()
    #     return "Swedish files scan started... "
    # except:
    #     return "Failed to scan Swedish files"
    scan()

def bgScanNl():
    from src.apis.scan_nl import scan
    # try:
    #     thread = threading.Thread(target=scan)
    #     thread.start()
    #     return "Dutch files scan started... "
    # except:
    #     return "Failed to scan Dutch files"
    scan()


# def bgPosQuery(cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic):
#     try:
#         thread = threading.Thread(target=positionQuery,
#                                   args = (cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic))
#         thread.start()
#         return "Querying... "
#     except:
#         return "Failed to start query"
#

# def bgInfoQuery(cow_id, grp, stats, start_date, end_date, fields, type):
#     try:
#         thread = threading.Thread(target=infoQuery,
#                                   args=(cow_id, grp, stats, start_date, end_date, fields, type))
#         thread.start()
#         return "Querying... "
#     except:
#         return "Failed to start query"
#
# def bgDrctQuery(statement):
#     try:
#         thread = threading.Thread(target=directQuery, args=statement)
#         thread.start()
#         return "Querying... "
#     except:
#         return "Failed to start query"