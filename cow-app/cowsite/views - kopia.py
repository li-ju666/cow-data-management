from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
#from django.conf import settings
import functions


def index(request):
   return render(request, "base.html",{})



def upload(request):
   context = {}
   if request.method == 'POST':
      uploaded_file = request.FILES['document']
      print("File uploaded:", uploaded_file.name)
      print("File size:", uploaded_file.size, "bytes")
      fs = FileSystemStorage()
      name = fs.save(uploaded_file.name, uploaded_file)
      context['url'] = fs.url(name)
   return render(request, 'upload.html', context)


def dbtest(request):
   if request.method == 'POST':
      try:

         cow_id = request.POST['cow_id']
         if cow_id is '':
            print('empty cowid')
         args = {}
         print('Trying to connect to database...')
         
         position_choice = request.POST['Position_data']

         if position_choice == 'PC':
            context = {
               "data" : functions.readDB(position_choice, cow_id),
               "data_header" : [' tag_str ',' start_time ',' end_time ',' posX ',' posY ',' posZ '],
               "position_choice" : position_choice
            }

         if position_choice == 'PA':
            context = {
               "data" : functions.readDB(position_choice, cow_id),
               "data_header" : [' tag_str ',' start_time ',' end_time ',' posX ',' posY ',' posZ ',' activity_type ',' distance '],
               "position_choice" : position_choice
            }

         if position_choice == 'FA':
            context = {
            "data" : functions.readDB(position_choice, cow_id),
            "data_header" : [' tag_str ',' measure_time ',' posX ',' posY ',' posZ '],
            "position_choice" : position_choice
            }
         
         if position_choice == 'PAA':
            context = {
            "data" : functions.readDB(position_choice, cow_id),
            "data_header" : [' tag_str ',' measure_time ',' interv ',' activity_type ',' distance ', ' period ', ' duration '],
            "position_choice" : position_choice
            }
      


         return render(request, "dblist/dblist.html", context)
      except Exception as e:
         print('Error occured:')
         print(e)
         return render(request, "dblist/dblist_fail.html")
      #finally:

   else:
      return render(request, "dblist/dblist_blank.html",{})