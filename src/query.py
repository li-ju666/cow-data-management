from src.lib.dbinit import connect
import datetime
from collections import namedtuple

# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: string, arg4 = position_type: [string],
# arg5 = start_date: string (yy-mm-dd), arg6 = end_date: string(yy-mm-dd), arg7 = start_time:string(hour:min:sec),
# arg8 = end_time:string(hour:min:sec), arg9 = periodic:bool



def positionQuery(cow_id, grp, stat, types, start_date, end_date, start_time, end_time, period):
    def quote(x):
        return '"' + x + '"'
    db = connect()
    cur = db.cursor()
    ############# TO DO: compare start and end date-time

    raw_records = []
    start_date = datetime.datetime.strptime(start_date, "%y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%y-%m-%d")

    localStart = (start_date - datetime.timedelta(days=7)).strftime("%y-%m-%d")
    localEnd = end_date.strftime("%y-%m-%d")
    if len(cow_id):
        for i in cow_id:
            cur = db.cursor()
            statement = 'SELECT cowID, insertDate, stat FROM CowInfo WHERE cowID = ' + str(i) + \
                        ' AND insertDate > ' + quote(localStart) + ' AND insertDate <= ' + quote(localEnd)
            cur.execute(statement)
            raw_records += cur.fetchall()
            cur.close()
    else:
        for i in grp:
            cur = db.cursor()
            # WHERE grp = 5 AND insertDate > (startDate - 7) AND insertDate <= (endDate)
            statement = 'SELECT cowID, insertDate, stat FROM CowInfo WHERE grp = ' + str(i) + \
                        ' AND insertDate > ' + quote(localStart) + ' AND insertDate <= ' + quote(end_date)
            # print(statement)
            cur.execute(statement)
            raw_records += cur.fetchall()
            cur.close()
    raw_records = list(map(list, raw_records))
    if stat != "all":
        raw_records = list(filter(lambda x: x[2] == stat, raw_records))
    def elementDateInsect(x):
        x[2] = x[1]+datetime.timedelta(days=7)
        x[1], x[2] = dateIntersect(x[1], x[2], start_date, end_date)
        return x
    raw_records = list(map(elementDateInsect, raw_records))

    return raw_records

def dateIntersect(start1, end1, start2, end2):
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    return latest_start, earliest_end

a = positionQuery([601, 611, 659], [11, 30], "DRÄKT", 4, "20-09-22", "20-10-06", 7, 8, 9)
for i in a:
    print(i)
