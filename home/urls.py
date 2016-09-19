'''
Created on 22.06.2016

@author: Moustafa Shama
'''

from django.conf.urls import url

from . import views


app_name = 'home'

urlpatterns = [
    url(r'^$', views.index, name='index'),
]