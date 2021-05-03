def write_query_log(query_type,user_inputs,file_names):
    import os
    with open('log/query_log.txt', 'a+') as f:
        f.write(query_type + '\n' + '[Result files]: '+file_names+'\n' +'[Inputs]: \n' + ' \n'.join(user_inputs) + '\n======================================================================================\n')
        f.close()

def read_query_log():
    f = open('log/query_log.txt','r')
    content = f.readlines()
    f.close()
    return content

def clear_query_log():
    open('log/query_log.txt','w').close()

def query_log_isempty():
    import os
    return os.stat("log/query_log.txt").st_size == 0

def download_log_file():
    from django.http import HttpResponse
    path = 'log/query_log.txt'
    response = HttpResponse(open(path, 'rb').read())
    response['Content-Disposition'] = 'attachment; filename='+'query_log.txt'
    response['Content-Type'] = 'text/plain'
    return response


def sort_files_by_time(files):
    import os
    files_absolute = [] #with absolute path
    for f in files:
        files_absolute.append('result_files/' + f)
    files_absolute.sort(key=os.path.getctime)
    files_ordered = []
    for f in files_absolute:
        files_ordered.append(f.replace("result_files/",""))
    return files_ordered[::-1]

def handle_uploaded_file(f,temp_dest):
    temp_dest = 'upload_files/' + temp_dest
    with open(temp_dest + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def format_overview_se(stat):
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

def format_overview_nl(stat):
    def get1(l, idx):
        if idx >= len(l):
            return None
        else:
            return l[idx]
    maxPos = max(len(stat['FA']), len(stat['PA']), len(stat['PAA']), len(stat['PC']))
    list1 = [stat['Milk']]

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
    output_list = []
    requested_list = []

    query_successful = True
    fetch_message = ''
    user_inputs = []


    if "milking_station" in request.POST:
        output_list.append(True)
        requested_list.append('milking_station')
    else:
        output_list.append(False)

    if "produced_milk" in request.POST:
        output_list.append(True)
        requested_list.append('produced_milk')
    else:
        output_list.append(False)
    
    
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
    if status_list == [] or start_date == '' or end_date == '' or not any(output_list):
        query_successful = False
        fetch_message = 'User input missing: '
        if status_list == []:
            user_inputs.append('status type')
        if start_date == '':
            user_inputs.append('start date')
        if end_date == '':
            user_inputs.append('end date')
        if not any(output_list):
            user_inputs.append('requested output')
    else:
        user_inputs = ['Cow id: ' + cow_id, 'Group number: ' + group_nr,'Status types selected: ' + ' '.join(status_list),
        'Start date: ' + start_date, 'End date: ' + end_date,'Requested outputs: ' + ' '.join(requested_list)]
        fetch_message = 'User input:'


    context = {
        'cow_id': cow_id,
        'group_nr': group_nr,
        'start_date': start_date,
        'end_date': end_date,
        'status_list': status_list,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
        'output_list': output_list
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
    tag_str = request.POST['tag_str']


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



    if tag_str == '':
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
            user_inputs = ['Cow id: ' + cow_id, 'Group number: ' + group_nr,'Status types selected: ' + ' '.join(status_list), 'Position type(s): ' + ' '.join(position_list),'Start date: ' + start_date, 'End date: ' + end_date,
            'Start time: ' + start_time, 'End time: ' + end_time, 'Periodic: ' + str(periodic)]
            fetch_message = 'User inputs:'
    else:
        if start_date == '' or end_date == '' or start_time == '' or end_time == '' or position_list == []:
            query_successful = False
            fetch_message = 'When querying with Tag string date and time are required! User input missing: '
            if start_date == '':
                user_inputs.append('start date'),
            if end_date == '':
                user_inputs.append('end date')
            if start_time == '':
                user_inputs.append('start time')
            if end_time == '':
                user_inputs.append('end time')
            if position_list == []:
                user_inputs.append('position data')
        else:
            user_inputs = ['Tag string: ' + tag_str, 'Start date: ' + start_date, 'End date: ' + end_date,
            'Start time: ' + start_time, 'End time: ' + end_time, 'Position type(s): ' + ' '.join(position_list)]
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
        'tag_str': tag_str,
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
    #tag_str = request.POST['tag_str']

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
    #if tag_str == '':
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
    #else:
        #if start_date == '' or end_date == '':
            #query_successful = False
            #fetch_message = 'When querying with Tag string date is required! User input missing: '
            #if start_date == '':
                #user_inputs.append('start date'),
            #if end_date == '':
                #user_inputs.append('end date')
        #else:
            #user_inputs = ['Tag string: ' + tag_str, 'Start date: ' + start_date, 'End date: ' + end_date]
            #fetch_message = 'User inputs:'
    
    

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



# ------------ DUTCH PARAMETERS FUNCTIONS ------------------- #

def dutch_position_context(request):

    #status_list = []
    position_list = []
    start_time = request.POST['start_time']
    end_time = request.POST['end_time']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    tag_str = request.POST['tag_str']

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

    
    #if "all_types" in request.POST:
    #    status_list = [
    #        'REDO',
    #        'INSEM',
    #        'DRÄKT',
    #        'SKAUT',
    #        'SINLD',
    #        'RÅMLK',
    #        'TIDIG',
    #    ]

    #if "DRACHTIG" in request.POST:
        #status_list.append('DRACHTIG')

    #if "GEDEKT" in request.POST:
        #status_list.append('GEDEKT')


        # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    #if tag_str == '':
        #if  start_date == '' or end_date == '' or start_time=='' or end_time == '' or position_list == []:
            #query_successful = False
            #fetch_message = 'User input missing: '
            #if status_list == []:
                #user_inputs.append('status type')
            #if position_list == []:
                #user_inputs.append('position data')
            #if start_date == '':
                #user_inputs.append('start date'),
            #if end_date == '':
                #user_inputs.append('end date')
            #if start_time == '':
                #user_inputs.append('start time')
            #if end_time == '':
                #user_inputs.append('end time')
        #else:
           #user_inputs = ['Position type(s): ' + ' '.join(position_list),'Start date: ' + start_date, 'End date: ' + end_date,
            #'Start time: ' + start_time, 'End time: ' + end_time, 'Periodic: ' + str(periodic)]
            #fetch_message = 'User inputs:'
    #else:
    if tag_str == '' or start_date == '' or end_date == '' or start_time == '' or end_time == '' or position_list == []:
        query_successful = False
        fetch_message = 'To query for Dutch position data, all fields except Periodic must be used. User input missing: '
        if start_date == '':
            user_inputs.append('start date'),
        if end_date == '':
            user_inputs.append('end date')
        if start_time == '':
            user_inputs.append('start time')
        if end_time == '':
            user_inputs.append('end time')
        if position_list == []:
            user_inputs.append('position data')
        if tag_str == '':
            user_inputs.append('tag string')
    else:
        user_inputs = ['Tag string: ' + tag_str, 'Start date: ' + start_date, 'End date: ' + end_date,
        'Start time: ' + start_time, 'End time: ' + end_time,  'Position type(s): ' + ' '.join(position_list)]
        fetch_message = 'User inputs:'


    

    context = {
        'start_time': start_time,
        'end_time': end_time,
        'start_date': start_date,
        'end_date': end_date,
        'periodic': periodic,
        'position_list': position_list,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
        'tag_str': tag_str,
    }
    return context, query_successful


def dutch_milkdata_context(request):
    #status_list = []
    cow_id = request.POST['cow_id']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']

    query_successful = True
    fetch_message = ''
    user_inputs = []
    
    
    #if "all_types" in request.POST:
        #status_list = [
            #'REDO',
            #'INSEM',
            #'DRÄKT',
            #'SKAUT',
            #'SINLD',
            #'RÅMLK',
            #'TIDIG',
        #]

    #if "DRACHTIG" in request.POST:
        #status_list.append('DRACHTIG')

    #if "GEDEKT" in request.POST:
        #status_list.append('GEDEKT')
    

    # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    if start_date == '' or end_date == '':
        query_successful = False
        fetch_message = 'User input missing: '
        #if status_list == []:
            #user_inputs.append('status type')
        if start_date == '':
            user_inputs.append('start date')
        if end_date == '':
            user_inputs.append('end date')
    else:
        user_inputs = ['Cow id: ' + cow_id,'Start date: ' + start_date, 'End date: ' + end_date]
        fetch_message = 'User input:'

    context = {
        'cow_id': cow_id,
        'start_date': start_date,
        'end_date': end_date,
        #'status_list': status_list,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
    }
    
    return context, query_successful



def dutch_cowinfo_context(request): # Currently not in use
  
    STATUS = []
    output_list = []
    cow_id = request.POST['cow_id']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    insem_type = []

    user_inputs = []
    fetch_message = ''
    query_successful = True


    # -- STATUS LIST PARAMETERS -- #      

    if "DRACHTIG" in request.POST:
        STATUS.append('DRACHTIG')

    if "GEDEKT" in request.POST:
        STATUS.append('GEDEKT')



    # ---------------------- #


    # User feedback when "Fetch data" is pressed. Check for invalid inputs.
    if STATUS == [] or start_date == '' or end_date == '' or insem_type == []:
        query_successful = False
        fetch_message = 'User input missing: '
        if STATUS == []:
            user_inputs.append('status type')
        if start_date == '':
            user_inputs.append('start date')
        if end_date == '':
            user_inputs.append('end date')
        if insem_type == []:
            user_inputs.append('insemination type')
    else:
        user_inputs = ['Cow id: ' + cow_id,", ".join(['Status types selected: '] + STATUS), 'Start date: ' + start_date, 'End date: ' + end_date,
        ", ".join(['Requested outputs: '] + requested_list), 'Special field: ' + special_field_feedback]
        fetch_message = 'User input:'
    
    

    context = {
        'cow_id': cow_id,
        'start_date': start_date,
        'end_date': end_date,
        'STATUS': STATUS,
        'insem_type': insem_type,
        'fetch_message': fetch_message,
        'user_inputs': user_inputs,
    }
    return context, query_successful
