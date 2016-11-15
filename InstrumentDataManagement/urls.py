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
    url(r'^viewInstrument/$', views.viewInstrument, name='viewInstrument'),
    url(r'^viewInstrument/(?P<instrument_id>[0-9]+)/$', views.viewInstrument, name='viewInstrument'),
    url(r'^viewInstrument/(?P<instrument_id>[0-9]+)/(?P<msg>(.*))/$', views.viewInstrument, name='viewInstrument'),
    url(r'^addInstrumentSynonym/$', views.addInstrumentSynonym, name='addInstrumentSynonym'),
    url(r'^deltInstrumentSynonym/(?P<synonym_id>[0-9]+)/$', views.deltInstrumentSynonym, name='deltInstrumentSynonym'),
    url(r'^viewAssetClasses/$', views.viewAssetClasses, name='viewAssetClasses'),
    url(r'^viewAssetClasses/(?P<assetclass_id>[0-9]*)/$', views.viewAssetClasses, name='viewAssetClasses'),
    url(r'^newAssetClass/$', views.newAssetClass, name='newAssetClass'),
    url(r'^addInstrumentAssetClass/(?P<assetclass_id>[0-9]+)/$', views.addInstrumentAssetClass, name='addInstrumentAssetClass'),
    url(r'^deltInstrumentAssetClass/(?P<assetclass_id>[0-9]+)/$', views.deltInstrumentAssetClass, name='deltInstrumentAssetClass'),
]