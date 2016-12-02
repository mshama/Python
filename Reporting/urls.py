'''
Created on 30.11.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'Reporting'

urlpatterns = [
    url(r'^QELV/$', views.mainCalculations_QELV, name='QELV'),
    url(r'^KINI/$', views.mainCalculations_KINI, name='KINI'),
]