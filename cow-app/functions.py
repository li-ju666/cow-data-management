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

    query_successful = True
    fetch_message = ''
    user_inputs = []
    
    
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
    

    # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    if status_list == [] or start_date == '' or end_date == '':
        query_successful = False
        fetch_message = 'User input missing: '
        if status_list == []:
            user_inputs.append('status type')
        if start_date == '':
            user_inputs.append('start date')
        if end_date == '':
            user_inputs.append('end date')
    else:
        user_inputs = ['Cow id: ' + cow_id, 'Group number: ' + group_nr,",".join(['Status types selected: '] + status_list),'Start date: ' + start_date, 'End date: ' + end_date]
        fetch_message = 'User input:'

    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_date': start_date,
        'end_date': end_date,
        'status_list': status_list,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
    }
    
    return context, query_successful



def position_context(request):

    status_list = []
    position_list = []
    cow_id = request.POST['cow_id']
    group_nr = request.POST['group_nr']
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    fetch_message = ''
    user_inputs = []
    query_successful = True


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

        # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    if status_list == [] or start_date == '' or end_date == '' or start_time=='' or end_time == '' or position_list == []:
        query_successful = False
        fetch_message = 'User input missing: '
        if status_list == []:
            user_inputs.append('status type')
        if position_list == []:
            user_inputs.append('position data')
        if start_date == '':
            user_inputs.append('start date'),
        if end_date == '':
            user_inputs.append('end date')
        if start_time == '':
            user_inputs.append('start time')
        if end_time == '':
            user_inputs.append('end time')
    else:
        user_inputs = ['Cow id: ' + cow_id, 'Group number: ' + group_nr,",".join(['Status types selected: '] + status_list), ['Position type(s): '] + position_list,'Start date: ' + start_date, 'End date: ' + end_date,
        'Start time: ' + start_time, 'End time: ' + end_time, 'Periodic: ' + str(periodic)]
        fetch_message = 'User inputs:'
        

    

    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_time': start_time,
        'end_time': end_time,
        'start_date': start_date,
        'end_date': end_date,
        'periodic': periodic,
        'position_list': position_list,
        'status_list': status_list,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
    }
    return context, query_successful


def cowinfo_context(request):
  
    STATUS = []
    output_list = []
    special_field = request.POST['special_field']
    cow_id = request.POST['cow_id']
    group_nr = request.POST['group_nr']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    requested_list = []

    user_inputs = []
    fetch_message = ''
    query_successful = True


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
        requested_list.append('resp_nr')
    else:
        output_list.append(False)

    if "Group" in request.POST:
        output_list.append(True)
        requested_list.append('Group')
    else:
        output_list.append(False)

    if "status" in request.POST:
        output_list.append(True)
        requested_list.append('status')
    else:
        output_list.append(False)

    if "lactation_nr" in request.POST:
        output_list.append(True)
        requested_list.append('lactation number')
    else:
        output_list.append(False)
    
    if "kalvn_date" in request.POST:
        output_list.append(True)
        requested_list.append('kalvn date')
    else:
        output_list.append(False)

    
    if special_field == '0':
        special_field_feedback = 'General information'
    elif special_field == '1':
        special_field_feedback = 'Health data'
    else:
        special_field_feedback = 'Insemination data'

    # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    if STATUS == [] or start_date == '' or end_date == '' or not any(output_list):
        query_successful = False
        fetch_message = 'User input missing: '
        if STATUS == []:
            user_inputs.append('status type')
        if start_date == '':
            user_inputs.append('start date')
        if end_date == '':
            user_inputs.append('end date')
        if not any(output_list):
            user_inputs.append('requested output')
    else:
        user_inputs = ['Cow id: ' + cow_id, 'Group number: ' + group_nr,", ".join(['Status types selected: '] + STATUS), 'Start date: ' + start_date, 'End date: ' + end_date,
        ", ".join(['Requested outputs: '] + requested_list), 'Special field: ' + special_field_feedback]
        fetch_message = 'User input:'
    
    

    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_date': start_date,
        'end_date': end_date,
        'STATUS': STATUS,
        'output_list': output_list,
        'special_field': special_field,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
    }
    return context, query_successful