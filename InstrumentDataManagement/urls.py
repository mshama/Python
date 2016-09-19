'''
Created on 14.09.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'InstrumentDataManagement'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newInstrument/$', views.newInstrument, name='newInstrument'),
]