from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('upload_swedish/', views.upload_swedish, name='upload_swedish'),
    path('upload_dutch/', views.upload_dutch, name='upload_dutch'),
    path('swe_db/', views.swe_db, name='swe_db'),
    path('swe_position/', views.swe_position, name='swe_position'),
    path('swe_milkdata/', views.swe_milkdata, name='swe_milkdata'),
    path('swe_cowinfo/', views.swe_cowinfo, name='swe_cowinfo'),
    path('dutch_data/', views.dutch_data, name='dutch'),
    path('dutch_position/', views.dutch_position, name='dutch_position'),
    path('dutch_milkdata/', views.dutch_milkdata, name='dutch_milkdata'),
    path('dutch_cowinfo/', views.dutch_cowinfo, name='dutch_cowinfo'),
    path('overview/', views.overview, name='overview'),
    path('about/', views.about, name='about'),
    path('swe_mapping_info', views.swe_mapping_info, name='se_mapping_info')
]
