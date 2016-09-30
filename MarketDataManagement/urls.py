'''
Created on 14.09.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'MarketDataManagement'

urlpatterns = [
    url(r'^viewMapping/$', views.manageMapping, name='manageMapping'),
    url(r'^viewMapping/(active)/$', views.manageMapping, name='manageMapping'),
    url(r'^updateData/$', views.updateData, name='updateData'),
]