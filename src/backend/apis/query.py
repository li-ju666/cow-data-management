from src.backend.lib.dbinit import connect
import datetime
from pandas import DataFrame as df
from itertools import compress
import os

################################# helper functions ###########################################

# return a quoted string
def quote(x):
    return '"' + x + '"'


# function to query all cows with valid time ranges and required status
def cowQuery(cow_id, grp, stats, start_date, end_date):
    db = connect()

    raw_records = []
    start_date = datetime.datetime.strptime(start_date, "%y-%m-%d")
    end_date = datetime.datetime.strptime(end_date, "%y-%m-%d")

    localStart = (start_date - datetime.timedelta(days=7)).strftime("%y-%m-%d")
    localEnd = end_date.strftime("%y-%m-%d")
    if len(cow_id):
        # query by cow id
        for i in cow_id:
            cur = db.cursor()
            statement = 'SELECT cowID, insertDate, stat FROM CowInfo WHERE cowID = ' + str(i) + \
                        ' AND insertDate > ' + quote(localStart) + ' AND insertDate <= ' + quote(localEnd)
            cur.execute(statement)
            raw_records += cur.fetchall()
            cur.close()
    elif len(grp):
        # query by group no
        for i in grp:
            cur = db.cursor()
            # WHERE grp = 5 AND insertDate > (startDate - 7) AND insertDate <= (endDate)
            statement = 'SELECT cowID, insertDate, stat FROM CowInfo WHERE grp = ' + str(i) + \
                        ' AND insertDate > ' + quote(localStart) + ' AND insertDate <= ' + quote(localEnd)
            # print(statement)
            cur.execute(statement)
            raw_records += cur.fetchall()
            cur.close()
    else:
        # select all records between time range
        cur = db.cursor()
        # WHERE grp = 5 AND insertDate > (startDate - 7) AND insertDate <= (endDate)
        statement = 'SELECT cowID, insertDate, stat FROM CowInfo WHERE insertDate > ' + \
                    quote(localStart) + ' AND insertDate <= ' + quote(localEnd)
        # print(statement)
        cur.execute(statement)
        raw_records += cur.fetchall()
        cur.close()
    # convert tuple to list
    raw_records = list(map(list, raw_records))
    # filter status
    raw_records = list(filter(lambda x: x[2] in stats, raw_records))

    # define function to get date intersection of valid range of record and requested date range
    def DateInsectWithRequested(x):
        x[2] = x[1] + datetime.timedelta(days=7)
        x[1], x[2] = dateIntersect(x[1], x[2], start_date.date(), end_date.date())
        return x

    #  get date intersection of valid range of record and requested date range
    raw_records = list(map(DateInsectWithRequested, raw_records))
    # for each cow, merge all requested valid days
    cow_dateRange = {}
    for record in raw_records:
        if cow_dateRange.get(record[0]):
            cow_dateRange[record[0]] += (getDays(record[1], record[2]))
        else:
            cow_dateRange[record[0]] = getDays(record[1], record[2])

    # function to generate a list of days to several ranges
    def daysToRanges(l):
        if not l:
            return []
        l = sorted(list(set(l)))
        # print(l)
        ranges = []
        step = datetime.timedelta(days=1)
        start = l[0]
        last = l[0]
        for day in l:
            if day <= last + step:
                last = day
                continue
            else:
                ranges.append([start, last])
                start = day
                last = day
        ranges.append([start, last])
        return ranges

    # dictionary: key-cowid, value-a list of ranges requested
    cow_dateRange = {k: daysToRanges(v) for k, v in cow_dateRange.items()}
    return cow_dateRange


# query tags with valid ranges
def tagQuery(cow_id, grp, stats, start_date, end_date):
    db = connect()
    cow_dateRange = cowQuery(cow_id, grp, stats, start_date, end_date)

    def tagRangeInsect(range, tagInfo):
        if tagInfo[3] is None:
            tagEnd = datetime.date.today()
        else:
            tagEnd = tagInfo[3]
        start, end = dateIntersect(range[0], range[1], tagInfo[2], tagEnd)
        # print(tagEnd)
        return tagInfo[0], tagInfo[1], start, end

    # fetch reference table for tags
    results = []
    for i in cow_dateRange:
        # print(cow_dateRange[i])
        statement = 'SELECT * FROM Reference WHERE cowID = ' + str(i)
        cur = db.cursor()
        cur.execute(statement)
        refs = cur.fetchall()
        results += [tagRangeInsect(r, t) for r in cow_dateRange[i] for t in refs]
        cur.close()
    return results


# get the insersection of two date ranges
def dateIntersect(start1, end1, start2, end2):
    # print(start1, end1, start2, end2)
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    return latest_start, earliest_end


# get all days within a data range
def getDays(start, end):
    days = []
    step = datetime.timedelta(days=1)
    current = start
    while current <= end:
        days.append(current)
        current += step
    return days



############################### Query functions #############################################

######### position query function ####################

# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: [string], arg4 = position_type: [string],
# arg5 = start_date: string (yy-mm-dd), arg6 = end_date: string(yy-mm-dd), arg7 = start_time:string(hour:min:sec),
# arg8 = end_time:string(hour:min:sec), arg9 = periodic:bool
def positionQuery(cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic):
    print("Position query started")
    path = "result_files/"
    tagRanges = tagQuery(cow_id, grp, stats, start_date, end_date)
    queryDict = {}
    queryDict['FA'] = 'measure_time'
    queryDict['PA'] = 'start_time'
    queryDict['PAA'] = 'measure_time'
    queryDict['PC'] = 'start_time'
    db = connect()
    filenames = []
    for pType in types:
        filename = "requested_" + pType + '.csv'
        filenames.append(filename)
        try:
            f = open(path+filename)
            f.close()
            os.remove(path+filename)
        except IOError:
            print("No old files exist")

        for tag in tagRanges:
            # print(tag)
            start = tag[2].strftime("%y-%m-%d")
            end = tag[3].strftime("%y-%m-%d")
            if periodic:
                statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[1]) + \
                            ' AND date(' + queryDict[pType] + \
                            ') between ' + quote(start) + ' and ' + quote(end) + \
                            ' AND time(' + queryDict[pType] + \
                            ') between ' + quote(start_time) + ' and ' + quote(end_time)
            else:
                statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[1]) + \
                            ' AND ' + queryDict[pType] + \
                            ' between' + quote(start + ' ' + start_time) + ' and ' + quote(end + ' ' + end_time)
            print(statement)
            cur = db.cursor()
            cur.execute(statement)
            tmp = cur.fetchall()
            result = list(map(lambda x: [tag[0]] + list(x), tmp))
            data = df(result)
            if data.empty:
                continue
            else:
                data.to_csv(path+filename, index=False, header=False, mode='a')
        try:
            f = open(path+filename)
        except IOError:
            f = open(path+filename, "w")
            f.write("No records fetched")
        finally:
            f.close()
    return filenames


########### info query function #################

# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: [string]
# arg4 = start_date: string (yy-mm-dd), arg5 = end_date: string(yy-mm-dd)
# arg6 = fields: [string] - ["stat", "lakt", ...]
# args7 = dateType: Int

def infoQuery(cow_id, grp, stats, start_date, end_date, fields, type):
    print("Info query started")
    path = "result_files/"
    db = connect()
    cow_dateRange = cowQuery(cow_id, grp, stats, start_date, end_date)

    # function to get statement for each type
    def getStatement(type, cow, start, end):
        if type == 0:
            statement = "SELECT * FROM CowInfo WHERE " + \
                        "cowID = " + str(cow) + " AND " + \
                        "insertDate between " + quote(start) + " and " + quote(end)
        elif type == 1:
            statement = "SELECT * FROM CowInfo" + \
                        " INNER JOIN HealthInfo ON CowInfo.cowID = HealthInfo.cowID" \
                        " AND CowInfo.insertDate = HealthInfo.insertDate" + \
                        " WHERE HealthInfo.cowID = " + str(cow) + " AND" + \
                        " HealthInfo.insertDate between " + quote(start) + " and " + quote(end)
            return statement
        else:
            statement = "SELECT * FROM CowInfo" + \
                        " INNER JOIN InsemInfo ON CowInfo.cowID = InsemInfo.cowID" \
                        " AND CowInfo.insertDate = InsemInfo.insertDate" + \
                        " WHERE InsemInfo.cowID = " + str(cow) + " AND" + \
                        " InsemInfo.insertDate between " + quote(start) + " and " + quote(end)
        return statement

    results = []
    # query data for each cow and each time range one by one
    for cow, dates in cow_dateRange.items():
        for each in dates:
            start = each[0].strftime("%y-%m-%d")
            end = each[1].strftime("%y-%m-%d")
            cur = db.cursor()
            statement = getStatement(type, cow, start, end)
            print(statement)
            cur.execute(statement)
            # result = cur.fetchall()
            # results += result
            results += cur.fetchall()
            cur.close()
    allfields = ["cowID", "insertDate", "resp", "grp", "stat", "lakt", "kalvn_date"]
    fieldnames = [[], ["cowID", "insertDate", "7dag", "100dag", "handelse_day", "comments"],
                  ["insertDate", "gp", "avsinad", "insem_date", "sedan_insem", "insem_tjur", "forv_kalvn", "tid_ins",
                   "tid_mellan"]]
    fieldnames = list(map(lambda x: allfields + x, fieldnames))
    mask = [True, True] + fields + [False] + [True] * 20
    fieldnames = list(compress(fieldnames[type], mask))

    def filterAndTrans(x):
        x = list(compress(x, mask))
        x = [a.strftime("%y-%m-%d") if isinstance(a, datetime.date) else a for a in x]
        return x

    requested = list(map(filterAndTrans, results))
    prefix = ["info", "health", "insem"]
    filename = prefix[type] + "_requested.csv"
    data = df(requested)
    if data.empty:
        text_file = open(path + filename, "w")
        text_file.write("No records fetched")
        text_file.close()
    else:
        data.to_csv(path+filename, index=False, header=fieldnames)
    return requested

############## direct query function #########################

def directQuery(statement):
    db = connect()
    cur = db.cursor()
    try:
        cur.execute(statement)
    except Exception as e:
        return str(e)
    path = "result_files/"
    filename = "result.csv"
    result = cur.fetchall()

    result = df(result)
    if result.empty:
        text_file = open(path + filename, "w")
        text_file.write("No records fetched")
        text_file.close()
    else:
        result.to_csv(path+filename, header=False, index=False)
    return filename


# a = infoQuery([], [], ["DRÄKT"], "20-10-01", "20-10-12",
#               [True, False, True, False, True], 1)

# a = positionQuery([], [], ["DRÄKT"], ["FA"], "20-09-22", "20-09-29", "08:00:00", "09:00:00", False)
