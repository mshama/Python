'''
Created on 24.11.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'PortfolioPositionManagement'

urlpatterns = [
    url(r'^viewPortfolios/$', views.viewPortfolios, name='viewPortfolios'),
    url(r'^viewMandates/$', views.viewMandates, name='viewMandates'),
    url(r'^addMandate/$', views.addMandate, name='addMandate'),
]