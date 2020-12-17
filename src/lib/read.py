from pandas import read_csv
import numpy as np
import datetime as dt

def readPos(filename):
    data = read_csv(filename, sep=",")
    return np.array(data)

def readKO(filename):
    raw = read_csv(filename, encoding="ISO-8859-1")
    all = list(map(lambda x: list(filter(lambda y: y != '', x.split(" "))),
                   list(np.array(raw).astype(str)[:, 0])))
    lengths = list(map(len, all))
    # raw kolista data
    rawkolista = all[1:lengths.index(3)]
    # info about cows that are dried off / to be slaughtered
    others = all[all.index(['Sinkor', 'och', 'slaktkor', 'på', 'bete'])+3:-1]
    # kolista handler function to add NULL for missing values
    def kolistaHandle(x):
        if len(x) == 7:
            x.insert(2, 'NULL')
        return x[:8]
    kolista = list(map(kolistaHandle, rawkolista))
    # raw data of dried off cows
    rawsinld = list(filter(lambda x: x[2] == 'SINLD', others))
    def sinldHandle(x):
        if len(x) > 13:
            n = len(x)-13
            x = x[:9]+[' '.join(x[9:10+n])]+x[10+n:]
        return x
    sinld = list(map(sinldHandle, rawsinld))
    # raw data of cows to be slaughtered
    rawskaut = list(filter(lambda x: x[2] =='SKAUT', others))
    def skaultHandle(x):
        result = []+x[0:3]
        idx = 3
        if x[3] == '0':
            result.append('NULL')
            result.append(x[3])
            idx = 4
        else:
            result += x[3:5]
            idx = 5
        result += x[idx:idx+2]
        idx += 2
        if x[idx] == '0':
            result.append('NULL')
            result.append(x[idx])
            idx += 1
        else:
            result += x[idx:idx+2]
            idx += 2
        result.append(' '.join(x[idx:-2]))
        result += x[-2:]
        if result[-3] == '':
            result[-3] = 'NULL'
        result.insert(-2, 'NULL')

        return result

    skaut = list(map(skaultHandle, rawskaut))
    # return two parts in numpy array
    return np.array(kolista), np.array(skaut+sinld)

def readHealth(filename):
    # read health data from files and return results in numpy array
    file = open(filename, encoding="ISO-8859-1")
    raw = file.readlines()
    lines = []
    for i in raw:
        lines.append(i.split(sep=" "))
    def removeEmpty(x):
        return list(filter(lambda x: x != '' and x != '\n', x))
    lines = list(map(removeEmpty, lines))
    idx = lines.index(['nr', 'nr', 'dat', '7dag', '100dag', 'dag', 'datum', 'namn'])
    lines = lines[idx+1:]
    def healthHandle(x):
        result = x[:8]
        try:
            result.append(str(int(x[8])))
            idx = 9
        except:
            result.append("NULL")
            idx = 8
        result.append(' '.join(x[idx:]))
        return result
    lines = list(map(healthHandle, lines))
    return np.array(lines)

# all= readHealth("data/info/Översikt hälsotillstånd X 200921.txt")
# for i in all:
#      print(len(i))

def readAvkastfile(textfile, first_upload=False):
    # add date 0 2345 7 each time
    # exception first time upload?
    # 1st time Pattern: mon, - ,sat, fri, thu, wed, tue, - , sun, sat, fri, thu, wed, tue, mon, sun, sat
    # other Pattern: mon, - ,sat, fri, thu, wed, tue, - ,sun

    textfile_arr = textfile.split()
    date_str = textfile_arr[3]
    year = int("20" + date_str[0:2])
    month = int(date_str[2:4])
    day = int(date_str[4:6])

    tuple_list = []

    if not first_upload:
        # Currently assuming no data is missing
        array = np.genfromtxt(textfile, dtype=None, skip_header=4, skip_footer=5, missing_values='missing',
                              autostrip=True, encoding="ISO-8859-1")
        for arr in array:
            cow_id = arr[0]
            delay = [0, 2, 3, 4, 5, 6, 8]
            for i in range(7):
                d = dt.datetime(year, month, day) - dt.timedelta(days=delay[i])
                tuple_list.append((str(cow_id), str(d), str(arr[i + 3])))

    else:
        array = np.genfromtxt(textfile, dtype=None, skip_header=4, skip_footer=5, missing_values='missing',
                              autostrip=True)
        for arr in array:
            cow_id = arr[0]
            delay = [0, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]
            for i in range(15):
                d = dt.datetime(year, month, day) - dt.timedelta(days=delay[i])
                tuple_list.append((str(cow_id), str(d), str(arr[i + 3])))
    return tuple_list


def readMjolkplatsfile(textfile):
    # Save file date
    textfile_arr = textfile.split()
    date_str = textfile_arr[1]
    year = int("20" + date_str[0:2])
    month = int(date_str[2:4])
    day = int(date_str[4:6])

    # Read lines, ignoring å ä ö
    file1 = open(textfile, 'r', errors='ignore', encoding="ISO-8859-1")
    lines = file1.readlines()

    n_max = len(lines) - 6
    n_line = 0

    # Use only wanted rows (skip 5 first and 5 last)
    # Creating list of cow_dicts with info + array
    tuple_list = []

    for line in lines:
        if (n_line > 4 and n_line < n_max):
            entry_list = line.split()
            if not entry_list:
                break  # Break if run out of lines
            cow_id = int(entry_list[0])
            status = entry_list[1]
            dim = int(entry_list[2])  # DIM not interesting?
            data = entry_list[3:]  # Get milking data in list
            milk_info_input = []  # List/array to upload

            missing = False  # not used
            wrong_order = False  # not used
            # CHECK THE DATA AND SET MISSING/WRONG_ORDER TRUE
            # Check status

            if (status == "SINLD"):  # Skip cows marked as dried off (status is updated when done milking)
                """
                dryoff_time = dt.datetime(year,month,day) - dt.datetime(2020,9,1) #REPLACE WITH ACTUAL DRY-OFF DATE
                if (dt.timedelta(days=7) > dryoff_time):
                    # For SINLD cows we adjust milking timestamps to morning milkings
                    # on monday, wednesday and friday. 
                    milkPlace = True
                    sinld = True
                    sinldShift = 0 # Shift days caused by SINLD-scheme
                    delay = 0.5
                    for elem in data:
                        if milkPlace:
                            mp = elem
                            milkPlace = False
                        else:
                            #Split timestamp into hours & minutes
                            split_str = elem.split(':')
                            #For the period of the cow being SINLD, data are recorded for
                            #monday, wednesday and friday
                            if sinld: #perhaps irrelavent/redundant
                                if (int(split_str[0]) < 12):
                                    if (sinldShift%7 == 0):
                                        d = dt.datetime(year,month,day) - dt.timedelta(days=sinldShift)
                                        t = dt.time(int(split_str[0]),minute=int(split_str[1]))
                                        milktime = dt.datetime.combine(d.date(),t)
                                        milkPlace = True
                                        tuple_list.append((str(cow_id),str(milktime), str(mp)))
                                        sinldShift += 3
                                    elif (sinldShift%7 == 3):
                                        d = dt.datetime(year,month,day) - dt.timedelta(days=sinldShift)
                                        t = dt.time(int(split_str[0]),minute=int(split_str[1]))
                                        milktime = dt.datetime.combine(d.date(),t)
                                        milkPlace = True
                                        tuple_list.append((str(cow_id),str(milktime), str(mp)))
                                        sinldShift += 2
                                    elif (sinldShift%7 == 5):
                                        d = dt.datetime(year,month,day) - dt.timedelta(days=sinldShift)
                                        t = dt.time(int(split_str[0]),minute=int(split_str[1]))
                                        milktime = dt.datetime.combine(d.date(),t)
                                        milkPlace = True
                                        tuple_list.append((str(cow_id),str(milktime), str(mp)))
                                        sinldShift += 2
                                    else:
                                        print("SINLD-shifting encountered an error")
                                else:
                                    #If the cow is no longer considered SINLD, then we
                                    #cannot match a milking to a date.
                                    sinld = False
                                    break
                else:
                    print(str(cow_id) + " not valid, since dryoff-date long ago")
                """
                n_line += 1
                continue
            elif (status == "TIDIG"):
                milkPlace = True
                delay = 0.5
                newRecords = []
                if not (len(data) == 30):
                    for elem in data:
                        if milkPlace:
                            mp = elem
                            milkPlace = False
                        else:
                            # Split timestamp into hours & minutes
                            split_str = elem.split(':')

                            # Check for shifted values
                            if (delay % 1 == 0):
                                if (int(split_str[0]) < 12):
                                    # print("small forbidden time value:",elem,"for TIDIG cow",cow_id)
                                    break
                            else:
                                if (int(split_str[0]) > 12):
                                    # print("large forbidden time value:",elem,"for TIDIG cow",cow_id)
                                    break

                            # Construct timestamp, counting backwards for date
                            # and reading timestamp for time.
                            d = dt.datetime(year, month, day) - dt.timedelta(days=np.floor(delay))
                            t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                            milktime = dt.datetime.combine(d.date(), t)
                            newRecords.append((str(cow_id), str(milktime), str(mp)))
                            delay += 0.5
                            milkPlace = True
                    tuple_list.extend(newRecords)  # Add non-shifted entries to list

                else:
                    for elem in data[:-2]:
                        if milkPlace:
                            mp = elem
                            milkPlace = False
                            newRecords = []
                        else:
                            # Split timestamp into hours & minutes
                            split_str = elem.split(':')

                            # Check for shifted values
                            if (delay % 1 == 0):
                                if (int(split_str[0]) < 12):
                                    # print("small forbidden time value:",elem,"for TIDIG cow",cow_id)
                                    break
                            else:
                                if (int(split_str[0]) > 12):
                                    # print("large forbidden time value:",elem,"for TIDIG cow",cow_id)
                                    break

                            # Construct timestamp, counting backwards for date
                            # and reading timestamp for time.
                            d = dt.datetime(year, month, day) - dt.timedelta(days=np.floor(delay))
                            t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                            milktime = dt.datetime.combine(d.date(), t)
                            newRecords.append((str(cow_id), str(milktime), str(mp)))
                            delay += 0.5
                            milkPlace = True
                    tuple_list.extend(newRecords)  # If no data was shifted, add to list
            elif (status == "DRKT"):
                # Check for 2-3 initial morning milkings -> assume to be dried off
                milkPlace = True
                delay = 0.5
                entry_index = 0
                sinld = False
                newRecords = []
                if not (len(data) == 30):
                    continue  # If not full columns, skip cow data assuming something's wrong
                for elem in data[:-2]:
                    if milkPlace:
                        mp = int(elem)
                        milkPlace = False
                    else:

                        # Split time into hours & minutes
                        split_str = elem.split(':')

                        # Check for shifted values
                        if (delay % 1 == 0):
                            if (int(split_str[0]) < 12):
                                # print("small forbidden time value:",elem,"for cow",cow_id)
                                if (entry_index == 1):
                                    sinld = True
                                else:
                                    break
                        else:
                            if (int(split_str[0]) > 12):
                                # print("large forbidden time value:",elem,"for cow",cow_id)
                                break

                        if (sinld):
                            # Construct timestamp, counting backwards for date
                            # following the dry-off scheme for a maximum of 3 entries
                            if (entry_index == 1):
                                d = dt.datetime(year, month, day) - dt.timedelta(days=3)
                                t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                                milktime = dt.datetime.combine(d.date(), t)
                                newRecords.append((str(cow_id), str(milktime), str(mp)))
                                delay += 0.5
                                milkPlace = True
                            elif (entry_index == 2):
                                d = dt.datetime(year, month, day) - dt.timedelta(days=5)
                                t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                                milktime = dt.datetime.combine(d.date(), t)
                                newRecords.append((str(cow_id), str(milktime), str(mp)))
                                delay += 0.5
                                milkPlace = True
                            else:
                                break

                        else:
                            # Construct timestamp, counting backwards for date
                            # and reading timestamp for time.
                            d = dt.datetime(year, month, day) - dt.timedelta(days=np.floor(delay))
                            t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                            milktime = dt.datetime.combine(d.date(), t)
                            newRecords.append((str(cow_id), str(milktime), str(mp)))
                            delay += 0.5
                            milkPlace = True
                        entry_index += 1
                tuple_list.extend(newRecords)  # Add non-shifted data to list
            else:
                milkPlace = True
                delay = 0.5
                newRecords = []
                if not (len(data) == 30):
                    continue  # If not full columns, skip cow data assuming something's wrong
                for elem in data[:-1]:
                    if milkPlace:
                        mp = int(elem)
                        milkPlace = False
                    else:
                        # Split time into hours & minutes
                        split_str = elem.split(':')

                        # Check for shifted values
                        if (delay % 1 == 0):
                            if (int(split_str[0]) < 12):
                                # print("small forbidden time value:",elem,"for cow",cow_id)
                                break
                        else:
                            if (int(split_str[0]) > 12):
                                # print("large forbidden time value:",elem,"for cow",cow_id)
                                break

                        # Construct timestamp, counting backwards for date
                        # and reading timestamp for time.
                        d = dt.datetime(year, month, day) - dt.timedelta(days=np.floor(delay))
                        t = dt.time(int(split_str[0]), minute=int(split_str[1]))
                        milktime = dt.datetime.combine(d.date(), t)
                        newRecords.append((str(cow_id), str(milktime), str(mp)))
                        delay += 0.5
                        milkPlace = True
                tuple_list.extend(newRecords)  # Add non-shifted data to list
        n_line += 1  # Count rows in for loop
    return tuple_list


# a = readAvkastfile('data/info/Avkastn 14 dag 200914.txt') #, first_upload=True) First file uploaded? set true to upload all entries
# c = readMjolkplatsfile('data/info/Mjölkplats 201026.txt')
#
# for i in c:
#     print(i)