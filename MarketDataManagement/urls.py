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
    url(r'^deactivateMapping/$', views.changeMappingActivation, name='editMapping'),
    url(r'^deactivateMapping/(?P<mapping_id>[0-9]+)/$', views.changeMappingActivation, name='changeMappingActivation'),
    url(r'^updateData/$', views.updateData, name='updateData'),
    url(r'^updateData/?source=(DS|BBG)$', views.updateData, name='updateData'),
]