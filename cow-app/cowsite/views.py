from django.shortcuts import render
from src.backend.apis.bgAPIs import bgInfoScan, bgPosScan, bgPosQuery, bgInfoQuery
from src.backend.apis.overview import overview_func, size_overview
from functions import format_overview, milkdata_context, position_context, cowinfo_context


def index(request):
   return render(request, "base.html",{})

def upload(request):
   context = {}
   if request.method == 'POST':
      if 'pos' in request.POST:
         context['pos'] = bgPosScan()
      if 'info' in request.POST:
         context['info'] = bgInfoScan()

   return render(request, 'upload.html', context)


def overview(request):
   over = overview_func()
   list_info, list_pos = format_overview(over)

   # list_size = [['CowInfo', 1489, '0.09 MB'], ['HealthInfo', 244, '0.05 MB'], ['FA', 0, '0.02 MB'], ['InsemInfo', 277, '0.02 MB'], ['MilkInfo', 0, '0.02 MB'], ['PA', 0, '0.02 MB'], ['PAA', 0, '0.02 MB'], ['PC', 0, '0.02 MB'], ['Reference', 249, '0.02 MB']]
   list_size = size_overview()
   context = {
      'info_header': ['KO','Health','Avkastn','Milk'],
      'position_header': ['FA','PA','PAA','PC'],
      'size_header': ['Table name', 'Nr of Records', 'Size (MB)'],
      'list_pos': list_pos,
      'list_info': list_info,
      'list_size': list_size,
   }
   return render(request, "overview.html", context)


def dblist(request):  
   return render(request, "dblist/dblist_blank.html",{})


def dblist_position(request):

   if request.method == 'POST':
      try:
         context = position_context(request)
         print(context)
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
         bgPosQuery(cow_id, grp, stats, types,
                    start_date, end_date, start_time, end_time, periodic)
      except Exception as error:
         print("Error:")
         print(error)

      finally:
         return render(request, "dblist/dblist_position.html", context)
   
   else:
      return render(request, "dblist/dblist_position.html", {})


def dblist_milkdata(request):

   if request.method == 'POST':
      try:
         print('innan')
         context = milkdata_context(request)
         print('efter')
         return render(request, "dblist/dblist_milkdata.html", context)
      except Exception as error:
         print("Error: ")
         print(error)
      finally:
         return render(request, "dblist/dblist_milkdata.html", context)
   else:
      return render(request, "dblist/dblist_milkdata.html", {})


def dblist_cowinfo(request):
 
   if request.method == 'POST':
      try:
         context = cowinfo_context(request)
         print(context)
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
         bgInfoQuery(cow_id, grp, stats, start_date, end_date, fields, type)
         return render(request, "dblist/dblist_cowinfo.html", context)
      except Exception as error:
         print("Error: ")
         print(error)

      finally:
         return render(request, "dblist/dblist_cowinfo.html", context)
   else:
      return render(request, "dblist/dblist_cowinfo.html", {})

   return render(request, "dblist/dblist_cowinfo.html", {})



def dutch_data(request):
   return render(request, "dutch_data/dutch_select.html",{})

def dutch_position(request):
   return render(request, "dutch_data/dutch_position.html", {})

def dutch_milkdata(request):
   return render(request, "dutch_data/dutch_milkdata.html", {})

def dutch_cowinfo(request):
   return render(request, "dutch_data/dutch_cowinfo.html", {})


def about(request):
   return render(request, 'about.html', {})
