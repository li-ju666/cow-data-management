from django.shortcuts import render
#<<<<<<< HEAD
from django.http import HttpResponse
from src.apis.bgAPIs import bgScanSe, bgPosQuery, bgInfoQuery
from src.apis.overview import overview_func, size_overview
from functions import format_overview, milkdata_context, position_context, cowinfo_context, handle_uploaded_file, dutch_position_context, dutch_milkdata_context, dutch_cowinfo_context
from src.apis.query import positionQuery, infoQuery, refQuery
from form import UploadFileForm
import os

#=======
#from src.apis.bgAPIs import bgScanSe, bgPosQuery, bgInfoQuery
#from src.apis.overview import overview_func, size_overview
#from functions import format_overview, milkdata_context, position_context, cowinfo_context
#from src.apis.query import positionQuery, infoQuery
#>>>>>>> b3ef5e0d19c70da209e6bdc4730c8e1b3357a2e2


def index(request):
   return render(request, "base.html",{})

def about(request):
   return render(request, 'about.html', {})

def file_scan(request):
   context = {}
   if request.method == 'POST':
      if 'pos' in request.POST:
         context['pos'] = bgScanSe()
      if 'info' in request.POST:
         context['info'] = bgScanSe()

   return render(request, 'file_scan.html', context)


# ---- Upload to database views ----------
def upload_swedish(request):
   file_names = []
   context = {}
   form = UploadFileForm()
   size_sum = 0
   context['status'] = 'Waiting for user input.'
   if request.method == 'POST':
      try:
         form = UploadFileForm(request.POST, request.FILES)
         files = request.FILES.getlist('files')
         if form.is_valid():
            for f in files:
               handle_uploaded_file(f,'se/')
               file_names.append(f.name)
            context['file_names'] = file_names
            
            #Estimate size of files
            for f in files:
               size_sum = size_sum + f.size

            #upload to swe database here
            bgScanSe() # Scan for swedish files to upload
            context['size_sum'] = 'Total size of files: {} MB'.format(size_sum/1000000)
            context['msg'] = 'File(s) submitted. The file will be visible in the Overview tab when it is successfully uploaded (for position data, this may take a while).'
            context['file_text'] = 'File(s) submitted:'
            context['status'] = 'Success!'
            
      except Exception as error:
         form = UploadFileForm()
         print('Error occured in upload_swe:')
         print(error)
         context['status'] = 'Error occured! The following message was past: "{}".'.format(error)
      finally:
         return render(request, 'upload/upload_swedish.html', context)
   return render(request, 'upload/upload_swedish.html', context)


def upload_dutch(request):
   file_names = []
   context = {}
   form = UploadFileForm()
   size_sum = 0
   context['status'] = 'Waiting for user input.'
   if request.method == 'POST':
      try:
         form = UploadFileForm(request.POST, request.FILES)
         files = request.FILES.getlist('files')

         if form.is_valid():
            for f in files:
               handle_uploaded_file(f,'nl/')
               file_names.append(f.name)
            context['file_names'] = file_names

         #Estimate size of files
         for f in files:
            size_sum = size_sum + f.size

         #upload to dutch database here
         context['size_sum'] = 'Total size of files: {} MB'.format(size_sum/1000000)
         context['msg'] = 'The following files have been passed to the database:'
         context['status'] = 'Success!'
      except Exception as error:
         form = UploadFileForm()
         print('Error occured in upload_dutch:')
         print(error)
         context['status'] = 'Error occured! The following message was past: "{}".'.format(error)
         
      
      finally:
         return render(request, 'upload/upload_dutch.html', context)
   return render(request, 'upload/upload_dutch.html', context)


def overview(request):
   context = {}
   try:
      over = overview_func()
      list_info, list_pos = format_overview(over)
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
def swe_db(request):  
   return render(request, "swe_data/swe_db.html",{})


def swe_position(request):

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
            if context['tag_str'] == '':
               tag_strs = []
            else:
               tag_strs = list(map(str, context['tag_str'].split(',')))

            stats = context['status_list']
            types = context['position_list']
            start_date = context['start_date']
            end_date = context['end_date']
            start_time = context['start_time']
            end_time = context['end_time']
            periodic = context['periodic']
           
            positionQuery(cow_id, grp, stats, types, tag_strs, start_date, end_date, start_time, end_time, periodic)
            context['status_message'] = 'Query was successful, file has been generated.'
         except Exception as error:
               print('Error: ')
               print(error)
               context['status_message'] = 'Failed to query, the following error message were passed: ' + str(error)
         finally:
            return render(request, "swe_data/swe_position.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "swe_data/swe_position.html", context)
   
   else:
      return render(request, "swe_data/swe_position.html", {})


def swe_milkdata(request):

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
            return render(request, "swe_data/swe_milkdata.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "swe_data/swe_milkdata.html", context)
   else:
      return render(request, "swe_data/swe_milkdata.html", {})


def swe_cowinfo(request):
 
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
            return render(request, "swe_data/swe_cowinfo.html", context)
      else:
         context['status_message'] = 'Mandatory input fields are missing, please try again.'
         return render(request, "swe_data/swe_cowinfo.html", context)

   else:
      return render(request, "swe_data/swe_cowinfo.html", {})



def swe_mapping_info(request):
   context = {}

   if request.method == 'POST':
      cow_id = request.POST['cow_id']
      if cow_id == '':
         context['msg'] = 'Cow ID is required to render table, try again!'
      else:
         try:
            cow_id = int(cow_id)
         except:
            context['msg'] = 'Incorrect format, Cow ID must be an integer! Your input:'
            context['msg_id'] = '{}'.format(cow_id)
            return render(request,'swe_data/swe_mapping_info.html', context)
         try:
            context['map_LoL'] = refQuery(cow_id)
            #context['map_LoL'] = [['tag1','date1','date1'],['tag2','date2','date2'],['tag3','date3','date3']]
            context['map_header'] = ['Tag Nr', 'Start date', 'End date']
            context['msg'] = 'Mapping info found!'
            context['msg_id'] = 'Rendering table using cow id = {}.'.format(cow_id)
         except Exception as error:
            context['msg'] = 'Error occured: {}'.format(error)
         finally:
            return render(request,'swe_data/swe_mapping_info.html', context)


   return render(request,'swe_data/swe_mapping_info.html', context)




# -------- DUTCH DATABASE -------------

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


