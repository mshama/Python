'''
Created on 25.11.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'ManualUpload'

urlpatterns = [
    url(r'^uploadData/$', views.uploadData, name='uploadData'),
]