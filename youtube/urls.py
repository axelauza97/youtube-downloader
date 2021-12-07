
from django.conf.urls import url,include
from django.urls import path, include

from . import views

urlpatterns = [
    path('',views.index, name='index'),
    path('download',views.download, name='download')
]
