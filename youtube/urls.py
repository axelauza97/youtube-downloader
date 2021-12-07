
from django.conf.urls import url,include
from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('playlist',views.playlist, name='playlist'),
    path('download',views.download, name='download'),
    path('downloads',views.downloads, name='downloads')
]
