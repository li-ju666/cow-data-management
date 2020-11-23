from src.lib.dbinit import connect
from time import time

start = time()
tags = ["'0024FA3C'", "'00250FDD'", "'00250D10'", "'0024F420'", "'0024F405'"]

db = connect()
# lengths = []
# for tag in tags:
#     queries = list(map(lambda x: "SELECT * FROM " + x + " WHERE tag_str = " + tag, ["PA", "PAA", "PC", "FA"]))
#     tmp = []
#     for query in queries:
#         cursor = db.cursor()
#         cursor.execute(query)
#         result = cursor.fetchall()
#         tmp.append(len(result))
#     lengths.append(tmp)
#     print(time()-start)
#
# print(time()-start)
# print(lengths)

start2 = time()
lengths2 = []
for tag in tags:
    query = "SELECT * FROM PC WHERE tag_str = " + tag + " AND start_time < '2020-09-18' AND start_time > '2020-09-15'"
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchall()
    lengths2.append(len(result))

print(time()-start2)
print(sum(lengths2))