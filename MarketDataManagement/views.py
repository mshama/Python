from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.db.models import Max
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# built in libraries
import pandas as pd
from _datetime import datetime

# own libraries
from dataconnections.datasource import get_metaData, get_PriceData

# model imports
from .models import MarketDataField_Mapping
from InstrumentDataManagement.models import Instrument

# form imports
from InstrumentDataManagement.forms import newMarketDataTypeForm
from MarketDataManagement.forms import newGoldenRecordFieldForm, newDatasourceFieldForm, newFieldMappingForm

# Create your views here.
def manageMapping(request, condition=''):
    if request.method == 'POST':
        if 'newFieldMapping' in request.POST:
            addMapping(request)
        elif 'newMarketDataType' in request.POST:
            newMarketDataType(request)
        elif 'newGoldenRecordField' in request.POST:
            newGoldenRecordField(request)
        elif 'newDatasourceField' in request.POST:
            newDatasourceField(request)
    
    if condition == 'active':
        marketdatafield_mapping = MarketDataField_Mapping.objects.exclude(valid_to__isnull=False)
    else:
        marketdatafield_mapping = MarketDataField_Mapping.objects.all()
    
    fieldMappingForm = newFieldMappingForm()
    marketDataTypeForm = newMarketDataTypeForm()
    goldenrecordfieldForm = newGoldenRecordFieldForm()
    datasourcefieldForm = newDatasourceFieldForm()
    context = {
               'field_mapping': marketdatafield_mapping,
               'fieldMappingForm': fieldMappingForm,
               'marketDataTypeForm': marketDataTypeForm,
               'goldenrecordfieldForm': goldenrecordfieldForm,
               'datasourcefieldForm': datasourcefieldForm,
    }
    return render(request, 'MarketDataManagement/viewMapping.html', context)
            
def addMapping(request):
    form = newFieldMappingForm(request.POST)
    if not form.save():
        return False
            
def newMarketDataType(request):
    form = newMarketDataTypeForm(request.POST)
    if not form.save():
        return False
    
def newGoldenRecordField(request):
    form = newGoldenRecordFieldForm(request.POST)
    if not form.save():
        return False

def newDatasourceField(request):
    form = newDatasourceFieldForm(request.POST)
    if not form.save():
        return False
    
def updateData(request):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST['currentInstrument'])
        source = request.POST['source']
        if 'fullData' in request.POST:
            fullData = request.POST['fullData']
        else:
            fullData = 'False'
        currentInstrument = Instrument.objects.filter(bbname=request.POST['currentInstrument'])[0]
        fields, lastPriceDate = get_instrumentData(source, currentInstrument)
        if fullData == 'True' or lastPriceDate is None:
            lastPriceDate = '2000-01-01'
        try:
            priceData = get_PriceData(source, currentInstrument.bbname, fields['fieldname'], lastPriceDate)
        
            insert_instrumentData(currentInstrument, fields['dbfieldname'], priceData)
            
            message = "update finished for:" + currentInstrument.description
        except Exception as e:
            message = "there was error updating:" + currentInstrument.description

        return HttpResponse(message)
    elif request.method == 'POST':
        if len(instrumentList) > 0:
            if 'fullData' in request.POST:
                fullData = request.POST['fullData']
            else:
                fullData = False
        elif 'newInstrumentList' in request.POST:
            instrumentList = request.POST['instrumentList']
            if 'fullData' in request.POST:
                fullData = True
            else:
                fullData = False
        elif 'instrumentList' in request.POST:
            selectedInstruments = request.POST.getlist('instrumentList')            
            instrumentList = pd.DataFrame(dict(zip(['bbname','description'], zip(*Instrument.objects.values_list('bbname','description').filter(id__in=selectedInstruments).order_by('description'))))).values.tolist()
            if 'fullData' in request.POST:
                fullData = True
            else:
                fullData = False
        else:
            instrumentList = pd.DataFrame(dict(zip(['bbname','description'], zip(*Instrument.objects.values_list('bbname','description').filter(source=request.POST['source']).order_by('description'))))).values.tolist()
            fullData = False
        context = {
                   'source': request.POST['source'],
                   'instrumentList': instrumentList,
                   'message': 'updating data',
                   'fullData': fullData,
                   'auto': 0,
                   }
        return render(request, 'DataManagementTool/updateData.html', context)
    elif request.method == 'GET':
        if 'source' in request.GET:
            if(request.GET['source']=='DS' or request.GET['source'] == 'BBG'):
                instrumentList = pd.DataFrame(dict(zip(['bbname','description'], zip(*Instrument.objects.values_list('bbname','description').filter(source=request.GET['source']).order_by('description'))))).values.tolist()
                context = {
                           'source': request.GET['source'],
                           'instrumentList': instrumentList,
                           'message': 'Automatic update',
                           'auto': 1,
                           }
                return render(request, 'DataManagementTool/updateData.html', context)
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            context = {
                       'msg': 'choice-page',
                       }
            return render(request, 'DataManagementTool/updateData.html', context)