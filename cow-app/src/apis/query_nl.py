from src.lib.dbmanager.dbinit import connect_nl
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
    db = connect_nl()

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
def tagQuery(cows):
    db = connect_nl()

    # fetch reference table for tags
    results = []
    for i in cows:
        # print(cow_dateRange[i])
        statement = 'SELECT * FROM Mapping WHERE ISO = ' + str(i).replace(" ", "") + " ORDER BY startDate"
        cur = db.cursor()
        cur.execute(statement)
        refs = list(map(list, cur.fetchall()))
        # results += [tagRangeInsect(r, t) for r in cow_dateRange[i] for t in refs]
        results += refs
        cur.close()
    return list(map(lambda x: x[2:], results))


def dateIntersect(range1, range2):
    startDate1, endDate1 = range1
    startDate2, endDate2 = range2
    if startDate1 > endDate2 or endDate1 < startDate2:
        return None
    elif startDate1 > startDate2:
        if endDate1 > endDate2:
            return (startDate1, endDate2)
        else:
            return (startDate1, endDate1)
    else:
        if endDate1 > endDate2:
            return (startDate2, endDate2)
        else:
            return (startDate2, endDate1)
############################### Query functions #############################################


# mapping query function
def refQuery(cow_id):
    refs = tagQuery([cow_id])
    return refs


# position query function
# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: [string], arg4 = position_type: [string],
# arg5 = start_date: string (yy-mm-dd), arg6 = end_date: string(yy-mm-dd), arg7 = start_time:string(hour:min:sec),
# arg8 = end_time:string(hour:min:sec), arg9 = periodic:bool
# return value: a list of tuples, each tuple is consisted of (filename, number of rows)
def positionQuery(cow_id, tags, types, start_date, end_date, start_time, end_time, periodic):
    print("Position query started")
    suffix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    path = "result_files/"

    start = datetime.datetime.strptime(start_date, "%y-%m-%d")
    end = datetime.datetime.strptime(end_date, "%y-%m-%d")
    if tags:
        # tagRanges: a list of tuple: (tag, startDate, endDate)
        tagRanges = list(map(lambda x: (x.replace(" ", ""), start, end), tags))
    else:
        tagRanges = []
        for each in tagQuery(cow_id):
            intersection = dateIntersect((each[1], each[2]), (start, end))
            if intersection:
                tagRanges.append((each[0], intersection[0], intersection[1]))
            else:
                continue

    queryDict = {}
    queryDict['FA'] = 'measure_time'
    queryDict['PA'] = 'start_time'
    queryDict['PAA'] = 'measure_time'
    queryDict['PC'] = 'start_time'
    db = connect_nl()
    query_result = []

    for pType in types:
        num_rows = 0
        filename = pType + suffix + '.csv'
        # filenames.append(filename)
        try:
            f = open(path+filename)
            f.close()
            os.remove(path+filename)
        except IOError:
            print("No old files exist")
        if not tagRanges:
            f = open(path+filename, "w")
            f.write("No records fetched")
        # else:
        #     f = open(path+filename, "w")
        #     for tag in tagRanges:
        #         print(tag, flush=True)
        #         start = tag[1].strftime("%y-%m-%d")
        #         end = tag[2].strftime("%y-%m-%d")
        #         f.write("  ".join([str(tag[0]), str(tag[1]), start, end])+"\n")
        # f.close()

        for tag in tagRanges:
            print(tag, flush=True)
            start = tag[1].strftime("%y-%m-%d")
            end = tag[2].strftime("%y-%m-%d")
            if periodic:
                statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[0]) + \
                            ' AND date(' + queryDict[pType] + \
                            ') between ' + quote(start) + ' and ' + quote(end) + \
                            ' AND time(' + queryDict[pType] + \
                            ') between ' + quote(start_time) + ' and ' + quote(end_time)
            else:
                statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[1]) + \
                            ' AND ' + queryDict[pType] + \
                            ' between' + quote(start + ' ' + start_time) + ' and ' + quote(end + ' ' + end_time)
            print(statement, flush=True)
            cur = db.cursor()
            cur.execute(statement)
            tmp = cur.fetchall()
            # result = list(map(lambda x: [tag[0]] + list(x), tmp))
            data = df(tmp)
            if data.empty:
                continue
            else:
                num_rows += len(data.index)
                data.to_csv(path+filename, index=False, header=False, mode='a')
        query_result.append((filename, num_rows))
    return query_result


############## milk query function ###########################
######## TOBE Verified!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
def milkQuery(cow_id, start_date, end_date):
    path = "result_files/"
    suffix = datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    db = connect_nl()

    return_value = []
    results = []
    for cow in cow_id:
        cur = db.cursor()
        statement = "SELECT * FROM MilkInfo WHERE levnr = {} AND " \
                    "insertDate between {} and {}".format(cow, quote(start_date), quote(end_date))
        print(statement, flush=True)
        cur.execute(statement)
        results += cur.fetchall()
        cur.close()
    data = df(results)
    filename = suffix + "milkinfo.csv"
    if data.empty:
        text_file = open(path + filename, "w")
        text_file.write("No records fetched")
        text_file.close()
    else:
        data.columns = ["diernr", "insertdate", "naam", "levnr", "kgmelk",
            "isk", "percentv", "eiw", "lact", "ur", "celget", "klfdat", "lftafk", "mprlft",
            "lactnr", "lactatiedagen", "kgmelklact", "kgmelk305", "vetlact", "vet305",
            "eiwlact", "eiw305", "kgvetlact", "kgvet305", "kgeiwlact", "kgeiw305", "lw"]
        data.to_csv(path+filename, index=False, header=True, sep=",")
    return_value.append((filename, len(data.index)))
    return return_value


############## direct query function #########################


def directQuery(statement):
    db = connect_nl()
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
