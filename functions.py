def format_overview(stat):
    def get1(l, idx):
        if idx >= len(l):
            return None
        else:
            return l[idx]
    maxInfo = max(len(stat['KO']), len(stat['Health']), len(stat['Avkastn']), len(stat['Milk']))
    maxPos = max(len(stat['FA']), len(stat['PA']), len(stat['PAA']), len(stat['PC']))
    list1 = []
    for i in range(maxInfo):
        tmp = []
        tmp.append(get1(stat['KO'], i))
        tmp.append(get1(stat['Health'], i))
        tmp.append(get1(stat['Avkastn'], i))
        tmp.append(get1(stat['Milk'], i))
        list1.append(tmp)
    list2 = []
    for i in range(maxPos):
        tmp = []
        tmp.append(get1(stat['FA'], i))
        tmp.append(get1(stat['PA'], i))
        tmp.append(get1(stat['PAA'], i))
        tmp.append(get1(stat['PC'], i))
        list2.append(tmp)
    return list1, list2


def milkdata_context(request):
    status_list = []
    cow_id = request.POST['cow_id']
    group_nr = request.POST['group_nr']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']     
    
    if "all_types" in request.POST:
        status_list = [
            'REDO',
            'INSEM',
            'DRÄKT',
            'SKAUT',
            'SINLD',
            'RÅMLK',
            'TIDIG',
        ]

    if "REDO" in request.POST:
        status_list.append('REDO')

    if "INSEM" in request.POST:
        status_list.append('INSEM')

    if "DRÄKT" in request.POST:
        status_list.append('DRÄKT')

    if "SKAUT" in request.POST:
        status_list.append('SKAUT')

    if "SINLD" in request.POST:
        status_list.append('SINLD')

    if "RÅMLK" in request.POST:
        status_list.append('RÅMLK')

    if "TIDIG" in request.POST:
        status_list.append('TIDIG')
   
    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_date': start_date,
        'end_date': end_date,
        'status_list': status_list,
    }
    
    return context



def position_context(request):
    status_list = []
    position_list = []
    cow_id = request.POST['cow_id']
    group_nr = request.POST['group_nr']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']


    if "Periodic" in request.POST:
        periodic = True
    else:
        periodic = False


    if "PA" in request.POST:
        position_list.append('PA')

    if "PAA" in request.POST:
        position_list.append('PAA')

    if "FA" in request.POST:
        position_list.append('FA')

    if "PC" in request.POST:
        position_list.append('PC')


    
    if "all_types" in request.POST:
        status_list = [
            'REDO',
            'INSEM',
            'DRÄKT',
            'SKAUT',
            'SINLD',
            'RÅMLK',
            'TIDIG',
        ]

    if "REDO" in request.POST:
        status_list.append('REDO')

    if "INSEM" in request.POST:
        status_list.append('INSEM')

    if "DRÄKT" in request.POST:
        status_list.append('DRÄKT')

    if "SKAUT" in request.POST:
        status_list.append('SKAUT')

    if "SINLD" in request.POST:
        status_list.append('SINLD')

    if "RÅMLK" in request.POST:
        status_list.append('RÅMLK')

    if "TIDIG" in request.POST:
        status_list.append('TIDIG')

    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_time': start_time,
        'end_time': end_time,
        'start_date': start_date,
        'end_date': end_date,
        'periodic': periodic,
        'position_list': position_list,
        'status_list': status_list
    }
    return context


def cowinfo_context(request):
    STATUS = []
    output_list = []
    special_field = request.POST['special_field']
    cow_id = request.POST['cow_id']
    group_nr = request.POST['group_nr']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']     
    

    # -- STATUS LIST PARAMETERS -- #      
    if "all_types" in request.POST:
        STATUS = [
            'REDO',
            'INSEM',
            'DRÄKT',
            'SKAUT',
            'SINLD',
            'RÅMLK',
            'TIDIG',
        ]

    if "REDO" in request.POST:
        STATUS.append('REDO')

    if "INSEM" in request.POST:
        STATUS.append('INSEM')

    if "DRÄKT" in request.POST:
        STATUS.append('DRÄKT')

    if "SKAUT" in request.POST:
        STATUS.append('SKAUT')

    if "SINLD" in request.POST:
        STATUS.append('SINLD')

    if "RÅMLK" in request.POST:
        STATUS.append('RÅMLK')

    if "TIDIG" in request.POST:
        STATUS.append('TIDIG')

    # ---------------------- #

    # ---- Requested Output Parameters -------- #
    # List of booleans,
    # order: "resp", "grp", "stat", "lakt", "kalvn_date"
    if "resp_nr" in request.POST:
        output_list.append(True)
    else:
        output_list.append(False)

    if "Group" in request.POST:
        output_list.append(True)
    else:
        output_list.append(False)

    if "status" in request.POST:
        output_list.append(True)
    else:
        output_list.append(False)

    if "lactation_nr" in request.POST:
        output_list.append(True)
    else:
        output_list.append(False)
    
    if "kalvn_date" in request.POST:
        output_list.append(True)
    else:
        output_list.append(False)
    

    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_date': start_date,
        'end_date': end_date,
        'STATUS': STATUS,
        'output_list': output_list,
        'special_field': special_field,
    }
    return context