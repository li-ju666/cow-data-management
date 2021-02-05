from django.shortcuts import render
from django.http import HttpResponse
from src.backend.apis.bgAPIs import bgInfoScan, bgPosScan, bgPosQuery, bgInfoQuery
from src.backend.apis.overview import overview_func, size_overview
from functions import format_overview, milkdata_context, position_context, cowinfo_context, handle_uploaded_file, dutch_position_context, dutch_milkdata_context, dutch_cowinfo_context
from src.backend.apis.query import positionQuery, infoQuery
from form import UploadFileForm
import os



def index(request):
   return render(request, "base.html",{})

def about(request):
   return render(request, 'about.html', {})

def file_scan(request):
   context = {}
   if request.method == 'POST':
      if 'pos' in request.POST:
         context['pos'] = bgPosScan()
      if 'info' in request.POST:
         context['info'] = bgInfoScan()

   return render(request, 'file_scan.html', context)


def upload_swedish(request):
   file_names = []
   context = {}
   form = UploadFileForm()
   if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      files = request.FILES.getlist('files')
      if form.is_valid():
         print('in valid')
         for f in files:
            handle_uploaded_file(f,'se/')
            file_names.append(f.name)
         context['msg'] = 'Success! The following files have been passed to the database:'
         context['file_names'] = file_names
         return render(request, 'upload/upload_swedish.html', context)
      else:
         form = UploadFileForm()
   return render(request, 'upload/upload_swedish.html', {})

def upload_dutch(request):
   file_names = []
   context = {}
   form = UploadFileForm()
   if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      files = request.FILES.getlist('files')

      print(request.POST.get('files'))
      if request.POST.get('files') == 'upload':
         if form.is_valid():
            print('in valid')
            for f in files:
               handle_uploaded_file(f,'nl/')
               file_names.append(f.name)
            context['msg'] = 'Success! The following files have been passed to the database:'
            context['file_names'] = file_names
            context['file_size'] = files.size
            return render(request, 'upload/upload_dutch.html', context)
         else:
            form = UploadFileForm()
   return render(request, 'upload/upload_dutch.html', {})


def overview(request):
   context = {}
   try:
      over = overview_func()
      list_info, list_pos = format_overview(over)

      # list_size = [['CowInfo', 1489, '0.09 MB'], ['HealthInfo', 244, '0.05 MB'], ['FA', 0, '0.02 MB'], ['InsemInfo', 277, '0.02 MB'], ['MilkInfo', 0, '0.02 MB'], ['PA', 0, '0.02 MB'], ['PAA', 0, '0.02 MB'], ['PC', 0, '0.02 MB'], ['Reference', 249, '0.02 MB']]
      list_size = size_overview()
      print("Overview function working fine")
      context = {
         'info_header': ['KO','Health','Avkastn','Milk'],
         'position_header': ['FA','PA','PAA','PC'],
         'size_header': ['Table name', 'Nr of Records', 'Size (MB)'],
         'list_pos': list_pos,
         'list_info': list_info,
         'list_size': list_size,
      }
      # context['status_messsage'] = "Database connected"
   except Exception as error:
      print('Error: ')
      print(error)
      context = {
         'info_header': ['KO','Health','Avkastn','Milk'],
         'position_header': ['FA','PA','PAA','PC'],
         'size_header': ['Table name', 'Nr of Records', 'Size (MB)'],
         'list_pos': [],
         'list_info': [],
         'list_size': [],
      }
      context['status_message'] = 'Failed to connect to database, the following error message were passed: ' + str(error)
   finally:
      return render(request, "overview.html", context)




# --------- SWEDISH DATABASE ------------ #
def dblist(request):  
   return render(request, "dblist/dblist_blank.html",{})


def dblist_position(request):

   if request.method == 'POST':
      context, query_successful = position_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            if context['group_nr'] == '':
               grp = []
            else:
               grp = list(map(int, context['group_nr'].split(',')))

            stats = context['status_list']
            types = context['position_list']
            start_date = context['start_date']
            end_date = context['end_date']
            start_time = context['start_time']
            end_time = context['end_time']
            periodic = context['periodic']
            #bgPosQuery(cow_id, grp, stats, types,
                     #start_date, end_date, start_time, end_time, periodic)
            positionQuery(cow_id, grp, stats, types, start_date, end_date, start_time, end_time, periodic)
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
               print('Error: ')
               print(error)
               context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "dblist/dblist_position.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dblist/dblist_position.html", context)
   
   else:
      return render(request, "dblist/dblist_position.html", {})


def dblist_milkdata(request):

   if request.method == 'POST':
      context, query_successful = milkdata_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            if context['group_nr'] == '':
               grp = []
            else:
               grp = list(map(int, context['group_nr'].split(',')))
            
            # No function to query
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
            print('Error: ')
            print(error)
            context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "dblist/dblist_milkdata.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dblist/dblist_milkdata.html", context)
   else:
      return render(request, "dblist/dblist_milkdata.html", {})


def dblist_cowinfo(request):
 
   if request.method == 'POST':
      context, query_successful = cowinfo_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            if context['group_nr'] == '':
               grp = []
            else:
               grp = list(map(int, context['group_nr'].split(',')))
            stats = context['STATUS']
            start_date = context['start_date']
            end_date = context['end_date']
            fields = context['output_list']
            type = int(context['special_field'])
            #bgInfoQuery(cow_id, grp, stats, start_date, end_date, fields, type)
            infoQuery(cow_id, grp, stats, start_date, end_date, fields, type)
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
            print('Error: ')
            print(error)
            context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "dblist/dblist_cowinfo.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dblist/dblist_cowinfo.html", context)

   else:
      return render(request, "dblist/dblist_cowinfo.html", {})


def dutch_data(request):
   return render(request, "dutch_data/dutch_select.html",{})

def dutch_position(request):
   if request.method == 'POST':
      context, query_successful = dutch_position_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            

            stats = context['status_list']
            types = context['position_list']
            start_date = context['start_date']
            end_date = context['end_date']
            start_time = context['start_time']
            end_time = context['end_time']
            periodic = context['periodic']
            #query function call
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
               print('Error: ')
               print(error)
               context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "dutch_data/dutch_position.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dutch_data/dutch_position.html", context)
   
   else:
      return render(request, "dutch_data/dutch_position.html", {})
   return render(request, "dutch_data/dutch_position.html", {})




def dutch_milkdata(request):

   if request.method == 'POST':
      context, query_successful = dutch_milkdata_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            
            # No function to query
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
            print('Error: ')
            print(error)
            context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request,"dutch_data/dutch_milkdata.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dutch_data/dutch_milkdata.html", context)
   else:
      return render(request, "dutch_data/dutch_milkdata.html", {})

def dutch_cowinfo(request):
 
   if request.method == 'POST':
      context, query_successful = dutch_cowinfo_context(request)
      if query_successful == True:
         try:
            if context['cow_id'] == '':
               cow_id = []
            else:
               cow_id = list(map(int, context['cow_id'].split(',')))
            
            stats = context['STATUS']
            start_date = context['start_date']
            end_date = context['end_date']
            fields = context['output_list']
            insem_type = context['insem_type']
            
            # query function
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
            print('Error: ')
            print(error)
            context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "dutch_data/dutch_cowinfo.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "dutch_data/dutch_cowinfo.html", context)

   else:
      return render(request, "dutch_data/dutch_cowinfo.html", {})


