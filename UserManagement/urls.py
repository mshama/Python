'''
Created on 24.11.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'UserManagement'

urlpatterns = [
    url(r'^viewUsers/$', views.viewUsers, name='viewUsers'),
    url(r'^viewUsers/(?P<user_id>[0-9]+)/$', views.viewUsers, name='viewUsers'),
    url(r'^addUser/$', views.addUser, name='addUser'),
    url(r'^viewGroups/$', views.viewGroups, name='viewGroups'),
    url(r'^viewGroups/(?P<group_id>[0-9]+)/$', views.viewGroups, name='viewGroups'),
    url(r'^addGroup/$', views.addGroup, name='addGroup'),
    url(r'^viewFunctions/$', views.viewFunctions, name='viewFunctions'),
    url(r'^viewFunctions/(?P<function_id>[0-9]+)/$', views.viewFunctions, name='viewFunctions'),
    url(r'^addFunction/$', views.addFunction, name='addFunction'),
]