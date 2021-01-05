from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name="index"),
    path('upload/', views.upload, name='upload'),
    path('dblist/', views.dblist, name='dblist'),
    path('dblist_position/', views.dblist_position, name='dblist_position'),
    path('dblist_milkdata/', views.dblist_milkdata, name='dblist_milkdata'),
    path('dblist_cowinfo/', views.dblist_cowinfo, name='dblist_cowinfo'),
    path('dutch_data/', views.dutch_data, name='dutch'),
    path('dutch_position/', views.dutch_position, name='dutch_position'),
    path('dutch_milkdata/', views.dutch_milkdata, name='dutch_milkdata'),
    path('dutch_cowinfo/', views.dutch_cowinfo, name='dutch_cowinfo'),
    path('overview/', views.overview, name='overview'),
    path('about/', views.about, name='about')
]
