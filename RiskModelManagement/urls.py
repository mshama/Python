'''
Created on 24.11.2016

@author: Moustafa Shama
'''
from django.conf.urls import url

from . import views

app_name = 'RiskModelManagement'

urlpatterns = [
    url(r'^viewRiskfactors/$', views.viewRiskfactors, name='viewRiskfactors'),
    url(r'^viewRiskfactor/$', views.viewRiskfactor, name='viewRiskfactor'),
    url(r'^viewRiskfactor/(?P<riskfactor_id>[0-9]+)/$', views.viewRiskfactor, name='viewRiskfactor'),
    url(r'^addRiskfactor/$', views.addRiskfactor, name='addRiskfactor'),
    url(r'^editComposition/(?P<riskfactor_id>[0-9]+)/$', views.editRiskfactorComposition, name='editRiskfactorComposition'),
    url(r'^editMapping/(?P<riskfactor_id>[0-9]+)/$', views.editRiskfactorMapping, name='editRiskfactorMapping'),
    url(r'^deleteMapping/(?P<mapping_id>[0-9]+)/$', views.deleteRiskfactorMapping, name='deleteRiskfactorMapping'),
    url(r'^editRiskfactor/(?P<riskfactor_id>[0-9]+)/$', views.editRiskfactor, name='editRiskfactor'),
      url(r'^deleteRiskfactor/(?P<riskfactor_id>[0-9]+)/$', views.deleteRiskfactor, name='deleteRiskfactor'),
#     url(r'^viewFunctions/$', views.viewFunctions, name='viewFunctions'),
#     url(r'^viewFunctions/(?P<function_id>[0-9]+)/$', views.viewFunctions, name='viewFunctions'),
#     url(r'^addFunction/$', views.addFunction, name='addFunction'),
]