from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.db.models import Q
# from django.template.context_processors import request
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# built in libraries
# import pandas as pd
from _datetime import datetime
import re

# own libraries
from dataconnections.datasource import get_PriceData

# model imports
from .models import MarketDataField_Mapping 
from .models import MarketData_Equity_DataStream_C, MarketData_Fixed_Income_DataStream_C, MarketData_Derivative_DataStream_C, MarketData_InterestRate_DataStream_C, MarketData_Index_DataStream_C
from .models import MarketData_Equity_C, MarketData_Fixed_Income_C, MarketData_Derivative_C, MarketData_InterestRate_C, MarketData_Index_C
from .models import MarketData_Equity_Bloomberg_C, MarketData_Fixed_Income_Bloomberg_C, MarketData_Derivative_Bloomberg_C, MarketData_InterestRate_Bloomberg_C, MarketData_Index_Bloomberg_C
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
    # get data from the HTTP request
    form = newFieldMappingForm(request.POST)
    if form.is_valid():
        # check if there is any old mappings with the same criteria 
        old_mappings = MarketDataField_Mapping.objects.filter(goldenrecord_field=form.cleaned_data['goldenrecord_field'], marketdatatype=form.cleaned_data['marketdatatype'], valid_to_d__isnull=True)
        # disable the old mappings by setting the valid to date for them
        for mapping in old_mappings:
            mapping.valid_to_d = datetime.now().date().strftime('%Y-%m-%d')
            mapping.save()
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
    
def deactivateMapping(request, mapping_id=''):
    if request.method == 'GET':
        updatedMapping = MarketDataField_Mapping.objects.get(pk=mapping_id)
        if updatedMapping.valid_to_d is not None:
            # check if there is any old mappings with the same criteria 
            old_mappings = MarketDataField_Mapping.objects.filter(goldenrecord_field=updatedMapping.goldenrecord_field, marketdatatype=updatedMapping.marketdatatype, valid_to_d__isnull=True)
            # disable the old mappings by setting the valid to date for them
            for mapping in old_mappings:
                mapping.valid_to_d = datetime.now().date().strftime('%Y-%m-%d')
                mapping.save()
            valid_to = None
        else:
            valid_to = datetime.now().date().strftime('%Y-%m-%d')
        updatedMapping.valid_to_d = valid_to
        updatedMapping.save()
        return redirect('MarketDataManagement:manageMapping')
    
def updateData(request, instrumentList=[]):
    if request.method == 'POST' and request.is_ajax():
        print(request.POST['currentInstrument'])
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
            instrumentList = Instrumentsynonym.objects.filter(
                                                              codification__name_c=request.POST['source'] + '_Ticker', 
                                                              code_c__in=selectedInstruments
                                                              ).values(
                                                                       'instrument_id', 'instrument__name_c', 'code_c'
                                                                       ).annotate(max_validity_d=Max('validity_d'))
            if 'fullData' in request.POST:
                fullData = True
            else:
                fullData = False
        else:
            if(request.POST['source'] == 'DS'):
                instrumentList = list(Instrumentsynonym.objects.filter(
                                                                  codification__name_c='DS_Ticker'
                                                                  ).values(
                                                                           'instrument_id', 'instrument__name_c', 'code_c'
                                                                           ).annotate(max_validity_d=Max('validity_d')).all())
                instrumentList.extend(list(Instrumentsynonym.objects.filter(
                                                                  Q(codification__name_c='DS_Code')
                                                                  ).exclude(
                                                                            instrument__id__in=[instrument['instrument_id'] for instrument in instrumentList]
                                                                            ).values(
                                                                                       'instrument_id', 'instrument__name_c', 'code_c'
                                                                                       ).annotate(max_validity_d=Max('validity_d'))))
            elif request.POST['source'] == 'BBG':
                instrumentList = list(Instrumentsynonym.objects.filter(
                                                                  codification__name_c='BBG_Ticker'
                                                                  ).values(
                                                                           'instrument_id', 'instrument__name_c', 'code_c'
                                                                           ).annotate(max_validity_d=Max('validity_d')).all())
            fullData = False
        context = {
                   'source': request.POST['source'],
                   'instrumentList': instrumentList,
                   'message': 'updating data',
                   'fullData': fullData,
                   'auto': 0,
                   }
        return render(request, 'MarketDataManagement/updateData.html', context)
    elif request.method == 'GET':
        if 'source' in request.GET:
            if(request.GET['source'] == 'DS'):
                instrumentList = list(Instrumentsynonym.objects.filter(
                                                                  codification__name_c='DS_Ticker'
                                                                  ).values(
                                                                           'instrument_id', 'instrument__name_c', 'code_c'
                                                                           ).annotate(max_validity_d=Max('validity_d')).all())
                instrumentList.extend(list(Instrumentsynonym.objects.filter(
                                                                  Q(codification__name_c='DS_Code')
                                                                  ).exclude(
                                                                            instrument__id__in=[instrument['instrument_id'] for instrument in instrumentList]
                                                                            ).values(
                                                                                       'instrument_id', 'instrument__name_c', 'code_c'
                                                                                       ).annotate(max_validity_d=Max('validity_d'))))
            elif request.GET['source'] == 'BBG':
                instrumentList = list(Instrumentsynonym.objects.filter(
                                                                  codification__name_c='BBG_Ticker'
                                                                  ).values(
                                                                           'instrument_id', 'instrument__name_c', 'code_c'
                                                                           ).annotate(max_validity_d=Max('validity_d')).all())
            else:
                instrumentList = []
            context = {
                       'source': request.GET['source'],
                       'instrumentList': instrumentList,
                       'message': 'Automatic update',
                       'auto': 1,
                       }
            return render(request, 'MarketDataManagement/updateData.html', context)
        else:
            context = {
                       'msg': 'choice-page',
                       }
            return render(request, 'MarketDataManagement/updateData.html', context)

def get_instrumentFields(source, instrument):
    fields = MarketDataField_Mapping.objects.filter(marketdatatype=instrument.marketdatatype, datasource_field__data_source_c=source).exclude(valid_to_d__isnull=False).values('datasource_field__name_c')
    return [ field['datasource_field__name_c'] for field in fields ]

def get_instrumentData(source, instrument):
    try:
        # get instrument
        fields = get_instrumentFields(source, instrument)
        
        # get last price Date
        if(source == 'DS'):
            if(instrument.marketdatatype.type_c == 'Equity'):
                pricedate = MarketData_Equity_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Fixed_Income'):
                pricedate = MarketData_Fixed_Income_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'InterestRate'):
                pricedate = MarketData_InterestRate_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Derivative'):
                pricedate = MarketData_Derivative_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Index'):
                pricedate = MarketData_Index_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
        elif(source == 'BBG'):
            if(instrument.marketdatatype.type_c == 'Equity'):
                pricedate = MarketData_Equity_Bloomberg_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Fixed_Income'):
                pricedate = MarketData_Fixed_Income_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'InterestRate'):
                pricedate = MarketData_InterestRate_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Derivative'):
                pricedate = MarketData_Derivative_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Index'):
                pricedate = MarketData_Index_DataStream_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            
        return fields, pricedate['date__max']
    except Exception as e:
        print("error reading instrument data, instrument:" + instrument.bbname + ",source:" + source)   

def insert_instrumentData(instrument, priceData, source):
    if(source == 'DS'):
        if(instrument.marketdatatype.type_c == 'Equity'):
            priceDataTable = eval('MarketData_Equity_DataStream_C')
            goldenRecordTable = eval('MarketData_Equity_C')
        elif(instrument.marketdatatype.type_c == 'Fixed_Income'):
            priceDataTable = eval('MarketData_Fixed_Income_DataStream_C')
            goldenRecordTable = eval('MarketData_Fixed_Income_C')
        elif(instrument.marketdatatype.type_c == 'InterestRate'):
            priceDataTable = eval('MarketData_InterestRate_DataStream_C')
            goldenRecordTable = eval('MarketData_InterestRate_C')
        elif(instrument.marketdatatype.type_c == 'Derivative'):
            priceDataTable = eval('MarketData_Derivative_DataStream_C')
            goldenRecordTable = eval('MarketData_Derivative_C')
        elif(instrument.marketdatatype.type_c == 'Index'):
            priceDataTable = eval('MarketData_Index_DataStream_C')
            goldenRecordTable = eval('MarketData_Index_C')
            
        insert_data(instrument, priceData, priceDataTable, goldenRecordTable,source)
    elif(source == 'BBG'):
        if(instrument.marketdatatype.type_c == 'Equity'):
            priceDataTable = eval('MarketData_Equity_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Equity_C')
        elif(instrument.marketdatatype.type_c == 'Fixed_Income'):
            priceDataTable = eval('MarketData_Fixed_Income_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Fixed_Income_C')
        elif(instrument.marketdatatype.type_c == 'InterestRate'):
            priceDataTable = eval('MarketData_InterestRate_Bloomberg_C')
            goldenRecordTable = eval('MarketData_InterestRate_C')
        elif(instrument.marketdatatype.type_c == 'Derivative'):
            priceDataTable = eval('MarketData_Derivative_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Derivative_C')
        elif(instrument.marketdatatype.type_c == 'Index'):
            priceDataTable = eval('MarketData_Index_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Index_C')
        print('not supported')
        
def insert_data(instrument, priceData, priceDataTable, goldenRecordTable, source):
    # select mapping
    fieldMapping = MarketDataField_Mapping.objects.filter(marketdatatype=instrument.marketdatatype, valid_to_d__isnull=True, datasource_field__data_source_c=source)
    for index, priceRecord in priceData.iterrows():
        priceRecord = priceRecord.to_dict()        
        try:
            # select data source price record
            priceRecordDB = priceDataTable.objects.get(instrument=instrument, date=index.strftime('%Y-%m-%d'))
            for key in priceRecord:
                setattr(priceRecordDB, key, priceRecord[key])
            # update data source price record
            priceRecordDB.update(update_fields=priceRecord.keys())
        except Exception as e:
            try:
                # insert into data source table
                priceRecord.update({'instrument': instrument, 'date': index.strftime('%Y-%m-%d'), })
                priceRecordDB = priceDataTable(**priceRecord)
                priceRecordDB.save(force_insert=True)
            except Exception as e1:
                print("could not update or insert data for this instrument:" + instrument.name_c + ",on this date:" + index.strftime('%Y-%m-%d'))
        
        # try to insert golden records only if there is at least one existing field mapping
        if(len(fieldMapping) > 0):
            try:
                # select data source price record
                goldenRecordDB = goldenRecordTable.objects.get(instrument=instrument, date=index.strftime('%Y-%m-%d'))
                update_fields = []
                for fieldPair in fieldMapping:
                    field_name = re.sub('[^0-9a-zA-Z_]+', '_', fieldPair.datasource_field.name_c.lower())
                    setattr(goldenRecordDB, fieldPair.goldenrecord_field.name_c.lower(), priceRecord[field_name])
                    update_fields.append(fieldPair.goldenrecord_field.name_c.lower())
                # update golden record price record
                goldenRecordDB.update(update_fields)
            except Exception as e:
                try:
                    # insert into golden record table 
                    # populate golden record dictionary
                    goldenRecord = {'instrument': instrument, 'date': index.strftime('%Y-%m-%d'), }
                    for fieldPair in fieldMapping:
                        field_name = re.sub('[^0-9a-zA-Z_]+', '_', fieldPair.datasource_field.name_c.lower())
                        goldenRecord[fieldPair.goldenrecord_field.name_c.lower()] = priceRecord[field_name]
                    goldenRecordDB = goldenRecordTable(**goldenRecord)
                    goldenRecordDB.save(force_insert=True)
                except Exception as e1:
                    print("could not update or insert golden record data for this instrument:" + instrument.name_c + ",on this date:" + index.strftime('%Y-%m-%d'))
