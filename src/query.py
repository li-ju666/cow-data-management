from src.lib.dbinit import connect
import datetime
from pandas import DataFrame as df

# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: [string], arg4 = position_type: [string],
# arg5 = start_date: string (yy-mm-dd), arg6 = end_date: string(yy-mm-dd), arg7 = start_time:string(hour:min:sec),
# arg8 = end_time:string(hour:min:sec), arg9 = periodic:bool

def quote(x):
    return '"' + x + '"'

def tagQuery(cow_id, grp, stats, start_date, end_date):
    db = connect()
    ############# TO DO: compare start and end date-time

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
        x[2] = x[1]+datetime.timedelta(days=7)
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

    def tagRangeInsect(range, tagInfo):
        if tagInfo[3] == None:
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

def dateIntersect(start1, end1, start2, end2):
    # print(start1, end1, start2, end2)
    latest_start = max(start1, start2)
    earliest_end = min(end1, end2)
    return latest_start, earliest_end

def getDays(start, end):
    days = []
    step = datetime.timedelta(days = 1)
    current = start
    while current <= end:
        days.append(current)
        current += step
    return days


# arg1 = cow_id: [int], arg2 = group_no: [int], arg3 = status: [string], arg4 = position_type: [string],
# arg5 = start_date: string (yy-mm-dd), arg6 = end_date: string(yy-mm-dd), arg7 = start_time:string(hour:min:sec),
# arg8 = end_time:string(hour:min:sec), arg9 = periodic:bool
def positionQuery(cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic):
    tagRanges = tagQuery(cow_id, grp, stats, start_date, end_date)
    queryDict = {}
    queryDict['FA'] = 'measure_time'
    queryDict['PA'] = 'start_time'
    queryDict['PAA'] = 'measure_time'
    queryDict['PC'] = 'start_time'
    db = connect()
    filenames = []
    for pType in types:
        result = []
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
                # statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[1]) + \
                #     ' AND ' + queryDict[pType] + '>=' + quote(start+' '+start_time) + ' AND ' + \
                #             queryDict[pType] + '<=' + quote(end+' '+end_time)
                statement = 'SELECT * FROM ' + pType + ' WHERE tag_str = ' + quote(tag[1]) + \
                    ' AND ' + queryDict[pType] + \
                    ' between' + quote(start+' '+start_time) + ' and ' + quote(end+' '+end_time)
            print(statement)
            cur = db.cursor()
            cur.execute(statement)
            tmp = cur.fetchall()
            # result += tmp
            #print(type(tmp[0]))
            result += list(map(lambda x: [tag[0]] + list(x), tmp))
        filename = "requested_"+pType+'.csv'
        filenames.append(filename)
        data = df(result)
        data.to_csv(filename, index=False, header=False)
    return filenames

# a = positionQuery([601, 841], [11], ["DRÄKT"], ['PC', 'PA', 'PAA'], "20-09-22", "20-09-25", "08:15:00", "10:15:00", True)