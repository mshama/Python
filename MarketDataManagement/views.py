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
from .models import MarketDataField_Mapping, DatasourceField, MarketData_Stock_DataStream_C, MarketData_Bond_DataStream_C, MarketData_Derivative_DataStream_C, MarketData_InterestRate_DataStream_C
from InstrumentDataManagement.models import Instrument, Instrumentsynonym, Codification

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
        marketdatafield_mapping = MarketDataField_Mapping.objects.exclude(valid_to_d__isnull=False)
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
    
def updateData(request, instrumentList=[]):
    if request.method == 'POST' and request.is_ajax():
        try:
            print(request.POST['currentInstrument'])
        except Exception as e:
            print('Error')
        source = request.POST['source']
        if 'fullData' in request.POST:
            fullData = request.POST['fullData']
        else:
            fullData = 'False'
        currentInstrument = Instrumentsynonym.objects.filter(code_c=request.POST['currentInstrument'])[0]
        fields, lastPriceDate = get_instrumentData(source, currentInstrument.instrument)
        if fullData == 'True' or lastPriceDate is None:
            lastPriceDate = '2000-01-01'
        try:
            priceData = get_PriceData(source, currentInstrument.code_c, fields, lastPriceDate)
        
            insert_instrumentData(currentInstrument.instrument, priceData, source)
            
            message = "update finished for:" + currentInstrument.instrument.name_c
        except Exception as e:
            message = "there was error updating:" + currentInstrument.instrument.name_c

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
            instrumentList = Instrumentsynonym.objects.filter(codification__name_c=request.POST['source']+'_Ticker').values('instrument_id','instrument__name_c','code_c').annotate(max_validity_d=Max('validity_d'))
            fullData = False
        context = {
                   'source': request.POST['source'],
                   'instrumentList': list(instrumentList.all()),
                   'message': 'updating data',
                   'fullData': fullData,
                   'auto': 0,
                   }
        return render(request, 'MarketDataManagement/updateData.html', context)
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
                return render(request, 'MarketDataManagement/updateData.html', context)
            else:
                return HttpResponseNotFound('<h1>Page not found</h1>')
        else:
            context = {
                       'msg': 'choice-page',
                       }
            return render(request, 'MarketDataManagement/updateData.html', context)

def get_instrumentFields(source, instrument):
    fields =  MarketDataField_Mapping.objects.filter(marketdatatype=instrument.marketdatatype,datasource_field__data_source_c=source).exclude(valid_to_d__isnull=False).values('datasource_field__name_c')
    return [ field['datasource_field__name_c'] for field in fields ]

def get_instrumentData(source, instrument):
    try:
        # get instrument
        fields = get_instrumentFields(source, instrument)
        
        # get last price Date
        if(source == 'DS'):
            if(instrument.marketdatatype.type_c == 'Stock'):
                pricedate = MarketData_Stock_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Bond'):
                pricedate = MarketData_Bond_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'InterestRate'):
                pricedate = MarketData_InterestRate_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Derivative'):
                pricedate = MarketData_Derivative_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
        elif(source == 'BBG'):
            pricedate = '31-12-9999'
            
        return fields, pricedate['date__max']
    except Exception as e:
        print("error reading instrument data, instrument:"+instrument.bbname+",source:"+source)   

def insert_instrumentData(instrument, priceData, source):
    if(source == 'DS'):
        if(instrument.marketdatatype.type_c == 'Stock'):
            priceDataTable = eval('MarketData_Stock_DataStream_C')
        elif(instrument.marketdatatype.type_c == 'Bond'):
            priceDataTable = eval('MarketData_Bond_DataStream_C')
        elif(instrument.marketdatatype.type_c == 'InterestRate'):
            priceDataTable = eval('MarketData_InterestRate_DataStream_C')
        elif(instrument.marketdatatype.type_c == 'Derivative'):
            priceDataTable = eval('MarketData_Derivative_DataStream_C')
            
        insert_data(instrument, priceData, priceDataTable)
    elif(source == 'BBG'):
        print('not supported')
        
def insert_data(instrument, priceData, priceDataTable):
    for index, priceRecord in priceData.iterrows():
        priceRecord = priceRecord.to_dict()        
        try:
            priceRecordDB = priceDataTable.objects.get(instrument=instrument, date=index.strftime('%Y-%m-%d'))
            for key in priceRecord:
                setattr(priceRecordDB, key, priceRecord[key])
            priceRecordDB.update(update_fields=priceRecord.keys())
        except Exception as e:
            try:
                priceRecord.update({'instrument': instrument, 'date': index.strftime('%Y-%m-%d'),})
                priceRecordDB = priceDataTable(**priceRecord)
                priceRecordDB.save(force_insert=True)
            except Exception as e1:
                print("could not update or insert data for this instrument:"+instrument.bbname+",on this date:"+index.strftime('%Y-%m-%d'))  