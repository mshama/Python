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
    url(r'^viewPositions/$', views.viewPositions, name='viewPositions'),
    url(r'^editPosition/(?P<position_id>[0-9]+)/$', views.editPosition, name='editPosition'),
    url(r'^deletePosition/(?P<position_id>[0-9]+)/$', views.deletePosition, name='deletePosition'),
    url(r'^viewTransactions/$', views.viewTransactions, name='viewTransactions'),
    url(r'^editTransaction/(?P<transaction_id>[0-9]+)/$', views.editTransaction, name='editTransaction'),
    url(r'^deleteTransaction/(?P<transaction_id>[0-9]+)/$', views.deleteTransaction, name='deleteTransaction'),
    url(r'^addTransactions/$', views.addTransactions, name='addTransactions'),
]