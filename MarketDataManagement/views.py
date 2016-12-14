from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Max
from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist, FieldDoesNotExist
# from django.template.context_processors import request
# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db import models

# built in libraries
# import pandas as pd
from _datetime import datetime
import re
import numpy as np

# own libraries
from dataconnections.datasource import get_PriceData, get_static_BBG,\
    get_BBG_PriceData

from data_saving.saving_functions import new_instrument, alter_marketdata_table

# model imports
from .models import MarketDataField_Mapping 
from .models import MarketData_Equity_DataStream_C, MarketData_Fixed_Income_DataStream_C, MarketData_Derivative_DataStream_C,\
        MarketData_InterestRate_DataStream_C, MarketData_Index_DataStream_C
from .models import MarketData_Equity_C, MarketData_Fixed_Income_C, MarketData_Derivative_C, MarketData_InterestRate_C, \
        MarketData_Index_C
from .models import MarketData_Equity_Bloomberg_C, MarketData_Fixed_Income_Bloomberg_C, MarketData_Derivative_Bloomberg_C, \
        MarketData_InterestRate_Bloomberg_C, MarketData_Index_Bloomberg_C
from InstrumentDataManagement.models import Instrumentsynonym, Codification,\
    Marketdatatype

# form imports
from InstrumentDataManagement.forms import newMarketDataTypeForm
from MarketDataManagement.forms import newGoldenRecordFieldForm, newDatasourceFieldForm, newFieldMappingForm
import data_saving
from MarketDataManagement.models import DatabaseTable, DatasourceField,\
    DatabaseTable_DataSourceField_Mapping, GoldenRecordField,\
    DatabaseTable_GoldenRecordField_Mapping

def price2LogRet(price1, price2):
    try:
        r = np.log(price1/price2)
        return r
    except Exception:
        return None

# Create your views here.
def manageMapping(request, condition=''):
    errors = None
    if request.method == 'POST':
        if 'newFieldMapping' in request.POST:
            errors = addMapping(request)
        elif 'newMarketDataType' in request.POST:
            errors = newMarketDataType(request)
        elif 'newGoldenRecordField' in request.POST:
            errors = newGoldenRecordField(request)
        elif 'newDBField' in request.POST:
            errors = newDBField(request)
    
    if condition == 'active':
        marketdatafield_mapping = MarketDataField_Mapping.objects.exclude(valid_to_d__isnull=False)
    else:
        marketdatafield_mapping = MarketDataField_Mapping.objects.all()
        
    databasetable_list = DatabaseTable.objects.all().order_by('datasource_c')
    
    fieldMappingForm = newFieldMappingForm()
    marketDataTypeForm = newMarketDataTypeForm()
    goldenrecordfieldForm = newGoldenRecordFieldForm()
    datasourcefieldForm = newDatasourceFieldForm()
    context = {
               'databasetable_list': databasetable_list,
               'field_mapping': marketdatafield_mapping,
               'fieldMappingForm': fieldMappingForm,
               'marketDataTypeForm': marketDataTypeForm,
               'goldenrecordfieldForm': goldenrecordfieldForm,
               'datasourcefieldForm': datasourcefieldForm,
    }
    if errors:
        context['errors'] = errors
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

def newDBField(request):
    
    selectedDatasetables_id = request.POST.getlist('related_databasetables')
    
    field_type = request.POST['fieldtype']
    data_source = request.POST['data_source']
    field_name = request.POST['field_name']
    
    #prepare field parameters
    if field_type == 'DecimalField':
        max_digits = request.POST['max_digits']
        decimal_places = request.POST['decimal_places']
        field_parameters = 'max_digits=' + str(max_digits) + ',decimal_places=' + str(decimal_places)
    elif field_type == 'CharField':
        max_length = request.POST['max_length']
        field_parameters = 'max_length=' + str(max_length)
    else:
        field_parameters = None
    
    if data_source == 'GR':
        try:
            goldenrecord_field = GoldenRecordField.objects.get(name_c = field_name)
            goldenrecord_field.fieldtype_c = field_type
            goldenrecord_field.fieldparameters_c = field_parameters
            goldenrecord_field.save()
        except ObjectDoesNotExist:
            goldenrecord_field = GoldenRecordField(
                                               name_c = field_name,
                                               fieldtype_c = field_type,
                                               fieldparameters_c = field_parameters
                                               )
            goldenrecord_field.save()
        
        for databasetable_id in selectedDatasetables_id:
            databasetable = DatabaseTable.objects.get(pk=databasetable_id)
            DatabaseTable_GoldenRecordField_Mapping(databasetable=databasetable, goldenrecordfield=goldenrecord_field).save()
            alter_marketdata_table(databasetable.name_c, goldenrecord_field.name_c, goldenrecord_field.fieldtype_c, goldenrecord_field.fieldparameters_c)
    else:
        try:
            datasource_field = DatasourceField.objects.get(name_c = field_name)
            datasource_field.fieldtype_c = field_type
            datasource_field.fieldparameters_c = field_parameters
            datasource_field.save()
        except ObjectDoesNotExist:
            datasource_field = DatasourceField(
                                               name_c = field_name,
                                               data_source_c = data_source,
                                               fieldtype_c = field_type,
                                               fieldparameters_c = field_parameters
                                               )
            datasource_field.save()
        
        for databasetable_id in selectedDatasetables_id:
            databasetable = DatabaseTable.objects.get(pk=databasetable_id)
            DatabaseTable_DataSourceField_Mapping(databasetable=databasetable, datasourcefield=datasource_field).save()
            alter_marketdata_table(databasetable.name_c, datasource_field.name_c, datasource_field.fieldtype_c, datasource_field.fieldparameters_c)
    
    
def changeMappingActivation(request, mapping_id=''):
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
            valid_from = datetime.now().date().strftime('%Y-%m-%d')
        else:
            valid_to = datetime.now().date().strftime('%Y-%m-%d')
            valid_from = updatedMapping.valid_from_d
        updatedMapping.valid_to_d = valid_to
        updatedMapping.valid_from_d = valid_from
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
        instrumentSyns = Instrumentsynonym.objects.filter(code_c=request.POST['currentInstrument']).exclude(validity_d__isnull = True)
        for instrumentSyn in instrumentSyns:
            fields, lastPriceDate = get_instrumentData(source, instrumentSyn.instrument)
            
            if fullData == 'True' or lastPriceDate is None:
                lastPriceDate = '2000-01-01'
            try:
                priceData = get_PriceData(source, instrumentSyn.code_c, fields, lastPriceDate)
            
                insert_instrumentData(instrumentSyn, priceData, source)
                
                message = "update finished for:" + instrumentSyn.instrument.name_c
            except Exception as e:
                message = "there was error updating:" + instrumentSyn.instrument.name_c

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
                                                              ).exclude(
                                                                            validity_d__isnull=True
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
                                                                  ).exclude(
                                                                            validity_d__isnull=True
                                                                            ).values(
                                                                                     'instrument_id', 'instrument__name_c', 'code_c'
                                                                                     ).annotate(max_validity_d=Max('validity_d')).all())
                instrumentList.extend(list(Instrumentsynonym.objects.filter(
                                                                  Q(codification__name_c='DS_Code')
                                                                  ).exclude(
                                                                            validity_d__isnull=True
                                                                            ).exclude(
                                                                                      instrument__id__in=[instrument['instrument_id'] for instrument in instrumentList]
                                                                                      ).values(
                                                                                               'instrument_id', 'instrument__name_c', 'code_c'
                                                                                               ).annotate(max_validity_d=Max('validity_d'))))
            elif request.POST['source'] == 'BBG':
                instrumentList = list(Instrumentsynonym.objects.filter(
                                                                  codification__name_c='BBG_Ticker'
                                                                  ).exclude(
                                                                            validity_d__isnull=True
                                                                            ).values(
                                                                                     'instrument_id', 'instrument__name_c', 'code_c'
                                                                                     ).annotate(max_validity_d=Max('validity_d')).all())
            if 'fullData' in request.POST:
                fullData = True
            else:
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
    fields = MarketDataField_Mapping.objects.filter(
                                                    marketdatatype=instrument.marketdatatype, 
                                                    datasource_field__data_source_c=source
                                                    ).exclude(
                                                              valid_to_d__isnull=False
                                                              ).values('datasource_field__name_c')
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
                pricedate = MarketData_Fixed_Income_Bloomberg_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'InterestRate'):
                pricedate = MarketData_InterestRate_Bloomberg_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Derivative'):
                pricedate = MarketData_Derivative_Bloomberg_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            elif(instrument.marketdatatype.type_c == 'Index'):
                pricedate = MarketData_Index_Bloomberg_C.objects.values_list('date').filter(instrument=instrument).aggregate(Max('date'))
            
        return fields, pricedate['date__max']
    except Exception as e:
        print("error reading instrument data, instrument:" + instrument.bbname + ",source:" + source)   

def add_missing_pricetable_fields(price_table, fields_table):
    dbfields = eval(fields_table).objects.filter(databasetables__name_c=price_table._meta.db_table)
    
    for field in dbfields:
        field_type = eval('models.'+field.fieldtype_c )
        field_parameters = dict(e.split('=') for e in field.fieldparameters_c.split(','))
        for key, _ in field_parameters.items():
            field_parameters[key] = int(field_parameters[key])
        class_field = field_type(
                                 name=re.sub('[^0-9a-zA-Z_]+', '_', field.name_c.lower()), 
                                 db_column=field.name_c,
                                 **field_parameters
                                 )
        class_field.model = price_table
        class_field.column = field.name_c
        class_field.attname = class_field.name
        class_field.concrete = True
        try:
            price_table._meta.get_field(class_field.name)
        except FieldDoesNotExist:
            price_table._meta.add_field(class_field)

def insert_instrumentData(instrumentSyn, priceData, source):
    if(source == 'DS'):
        if(instrumentSyn.instrument.marketdatatype.type_c == 'Equity'):
            priceDataTable = eval('MarketData_Equity_DataStream_C')
            add_missing_pricetable_fields(priceDataTable,'DatasourceField')
            goldenRecordTable = eval('MarketData_Equity_C')
            add_missing_pricetable_fields(goldenRecordTable,'GoldenRecordField')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Fixed_Income'):
            priceDataTable = eval('MarketData_Fixed_Income_DataStream_C')
            goldenRecordTable = eval('MarketData_Fixed_Income_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'InterestRate'):
            priceDataTable = eval('MarketData_InterestRate_DataStream_C')
            goldenRecordTable = eval('MarketData_InterestRate_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Derivative'):
            priceDataTable = eval('MarketData_Derivative_DataStream_C')
            goldenRecordTable = eval('MarketData_Derivative_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Index'):
            priceDataTable = eval('MarketData_Index_DataStream_C')
            goldenRecordTable = eval('MarketData_Index_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Currency'):
            priceDataTable = eval('MarketData_Currency_DataStream_C')
            goldenRecordTable = eval('MarketData_Currency_C')
            
        insert_data(instrumentSyn, priceData, priceDataTable, goldenRecordTable,source)
    elif(source == 'BBG'):
        if(instrumentSyn.instrument.marketdatatype.type_c == 'Equity'):
            priceDataTable = eval('MarketData_Equity_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Equity_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Fixed_Income'):
            priceDataTable = eval('MarketData_Fixed_Income_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Fixed_Income_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'InterestRate'):
            priceDataTable = eval('MarketData_InterestRate_Bloomberg_C')
            goldenRecordTable = eval('MarketData_InterestRate_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Derivative'):
            priceDataTable = eval('MarketData_Derivative_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Derivative_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Index'):
            priceDataTable = eval('MarketData_Index_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Index_C')
        elif(instrumentSyn.instrument.marketdatatype.type_c == 'Currency'):
            priceDataTable = eval('MarketData_Currency_Bloomberg_C')
            goldenRecordTable = eval('MarketData_Currency_C')
        insert_data(instrumentSyn, priceData, priceDataTable, goldenRecordTable,source)
        
def insert_source_price_record(instrument, priceRecord, priceDataTable, price_date):
    try:
        # select data source price record
        priceRecordDB = priceDataTable.objects.get(instrument=instrument, date=price_date.strftime('%Y-%m-%d'))
        for key in priceRecord:
            setattr(priceRecordDB, key, priceRecord[key])
        # update data source price record
        priceRecordDB.save()
    except ObjectDoesNotExist as e:
        try:
            # insert into data source table
            priceRecord.update({'instrument': instrument, 'date': price_date.strftime('%Y-%m-%d'), })
            priceRecordDB = priceDataTable(**priceRecord)
            priceRecordDB.save(force_insert=True)
        except Exception as e1:
            print("could not update or insert data for this instrument:" + instrument.name_c + ",on this date:" + price_date.strftime('%Y-%m-%d'))
    except Exception as e:
        print('Error inserting new data source record' + str(priceRecord))

def update_future_golden_record(instrumentSyn, priceRecord, goldenRecordDB, price_date, update_fields, source):
    # get the suffix of the instrument (Index, Comdty, ..etc)
    instr_suffix = re.split(" ", instrumentSyn.code_c)[-1]
    
    # decides if any new instrument to be inserted if it is going to be active or not
    if price_date.date() == datetime.now().date():
        active = True
    else:
        active = False
    
    # try to find the current contract instrument
    try:
        current_contract_instrument = Instrumentsynonym.objects.get(code_c=priceRecord['fut_cur_gen_ticker']+" "+instr_suffix)
        if active and current_contract_instrument.validity_d == None:
            current_contract_instrument.validity_d = datetime.now().date()
            current_contract_instrument.save()
            # update the rest of synonyms that belong to this instrument
            synonyms = Instrumentsynonym.objects.filter(instrument=current_contract_instrument.instrument)
            for synonym in synonyms:
                synonym.validity_d = datetime.now().date()
                synonym.save()
        current_contract_instrument = current_contract_instrument.instrument
    except ObjectDoesNotExist as e:
        current_contract_instrument, _ = new_instrument(instrument_ticker=priceRecord['fut_cur_gen_ticker']+" "+instr_suffix, 
                                                  ticker_type=source, 
                                                  market_data_type='Contract Future',
                                                  currency=instrumentSyn.instrument.currency, 
                                                  underlying_curreny=instrumentSyn.instrument.underlying_currency,
                                                  active = active)
        
    setattr(goldenRecordDB, 'current_contract_instrument', current_contract_instrument)
    is_same, following_contract_instrument = is_same_contract(instrumentSyn.instrument, price_date.date(), current_contract_instrument)
    if is_same:
        synonyms = Instrumentsynonym.objects.filter(instrument=following_contract_instrument)
        for synonym in synonyms:
            if active and synonym.validity_d == None:
                synonym.validity_d = datetime.now().date()
                synonym.save()
        setattr(goldenRecordDB, 'following_contract_instrument', following_contract_instrument)
    else:
        # try to find the following contract instrument
        # get the prefix (eg from VG1 Index get VG1)
        instr_prefix = re.split(" ", instrumentSyn.code_c)[0]
        # get the second generic (eg from VG1 get VG2 Index)
        sec_instr = instr_prefix.replace('1','2') + ' ' + instr_suffix
        # get the current contract from bloomberg for the second generic
        fut_contract = get_BBG_PriceData(sec_instr,['FUT_CUR_GEN_TICKER'], price_date, price_date)['fut_cur_gen_ticker'][0] + ' ' + instr_suffix
        # find or create a new instrument with the current contract of the second generic
        try:
            following_contract_instrument = Instrumentsynonym.objects.get(code_c=fut_contract)
            if active and following_contract_instrument.validity_d == None:
                following_contract_instrument.validity_d = datetime.now().date()
                following_contract_instrument.save()
                # update the rest of synonyms that belong to this instrument
                synonyms = Instrumentsynonym.objects.filter(instrument=following_contract_instrument.instrument)
                for synonym in synonyms:
                    synonym.validity_d = datetime.now().date()
                    synonym.save()
            following_contract_instrument = following_contract_instrument.instrument
        except ObjectDoesNotExist as e:
            following_contract_instrument, _ = new_instrument(instrument_ticker=fut_contract, 
                                                          ticker_type=source, 
                                                          market_data_type='Contract Future',
                                                          currency=instrumentSyn.instrument.currency, 
                                                          underlying_curreny=instrumentSyn.instrument.underlying_currency,
                                                          active=active)
        setattr(goldenRecordDB, 'following_contract_instrument', following_contract_instrument)
    update_fields.extend(["current_contract_instrument", "following_contract_instrument"])
        # remove the fut_cur_gen_ticker from goldenRecord
    return goldenRecordDB, update_fields

def is_same_contract(instrument, current_date,  current_contract_instrument):    
    try:
        previous_record = MarketData_Derivative_C.objects.filter(instrument = instrument, date__lt = current_date).order_by('-date')[:1][0]
        if previous_record.current_contract_instrument.id == current_contract_instrument.id:
            return True, previous_record.following_contract_instrument
        else:
            return False, None
    except (ObjectDoesNotExist, IndexError):
        return False, None
    except Exception:
        return False, None
    

def new_future_golden_record(instrumentSyn, goldenRecord, price_date, source):
    try:
        # get the suffix of the instrument (Index, Comdty, ..etc)
        instr_suffix = re.split(" ", instrumentSyn.code_c)[-1]
        
        # decides if any new instrument to be inserted if it is going to be active or not
        if price_date.date() == datetime.now().date():
            active = True
        else:
            active = False
        
        # try to find the current contract instrument
        try:
            current_contract_instrument = Instrumentsynonym.objects.get(code_c=goldenRecord['current_contract_instrument']+" "+instr_suffix)
            if active and current_contract_instrument.validity_d == None:
                current_contract_instrument.validity_d = datetime.now().date()
                current_contract_instrument.save()
                # update the rest of synonyms that belong to this instrument
                synonyms = Instrumentsynonym.objects.filter(instrument=current_contract_instrument.instrument)
                for synonym in synonyms:
                    synonym.validity_d = datetime.now().date()
                    synonym.save()
            current_contract_instrument = current_contract_instrument.instrument
        except ObjectDoesNotExist as e:
            current_contract_instrument, _ = new_instrument(instrument_ticker=goldenRecord['current_contract_instrument']+" "+instr_suffix, 
                                                      ticker_type=source, 
                                                      market_data_type='Contract Future',
                                                      currency=instrumentSyn.instrument.currency, 
                                                      underlying_curreny=instrumentSyn.instrument.underlying_currency,
                                                      active = active)
            
        goldenRecord['current_contract_instrument'] = current_contract_instrument
        is_same, following_contract_instrument = is_same_contract(instrumentSyn.instrument, price_date.date(), current_contract_instrument)
        if is_same:
            synonyms = Instrumentsynonym.objects.filter(instrument=following_contract_instrument)
            for synonym in synonyms:
                if active and synonym.validity_d == None:
                    synonym.validity_d = datetime.now().date()
                    synonym.save()
            goldenRecord['following_contract_instrument'] = following_contract_instrument
        else:
            # try to find the following contract instrument
            # get the prefix (eg from VG1 Index get VG1)
            instr_prefix = re.split(" ", instrumentSyn.code_c)[0]
            # get the second generic (eg from VG1 get VG2 Index)
            sec_instr = instr_prefix.replace('1','2') + ' ' + instr_suffix
            # get the current contract from bloomberg for the second generic
            fut_contract = get_BBG_PriceData(sec_instr,['FUT_CUR_GEN_TICKER'], price_date, price_date)['fut_cur_gen_ticker'][0] + ' ' + instr_suffix
            # find or create a new instrument with the current contract of the second generic
            try:
                following_contract_instrument = Instrumentsynonym.objects.get(code_c=fut_contract)
                if active and following_contract_instrument.validity_d == None:
                    following_contract_instrument.validity_d = datetime.now().date()
                    following_contract_instrument.save()
                    # update the rest of synonyms that belong to this instrument
                    synonyms = Instrumentsynonym.objects.filter(instrument=following_contract_instrument.instrument)
                    for synonym in synonyms:
                        synonym.validity_d = datetime.now().date()
                        synonym.save()
                following_contract_instrument = following_contract_instrument.instrument
            except ObjectDoesNotExist as e:
                following_contract_instrument, _ = new_instrument(instrument_ticker=fut_contract, 
                                                              ticker_type=source, 
                                                              market_data_type='Contract Future',
                                                              currency=instrumentSyn.instrument.currency, 
                                                              underlying_curreny=instrumentSyn.instrument.underlying_currency,
                                                              active=active)
            except Exception as e1:
                pass
            goldenRecord['following_contract_instrument'] = following_contract_instrument
    except Exception as e:
        pass
        
    return goldenRecord
     
def insert_golden_record(instrumentSyn, priceRecord, goldenRecordTable, fieldMapping, price_date, source, previous_price):
    try:
        # select data source price record
        goldenRecordDB = goldenRecordTable.objects.get(instrument=instrumentSyn.instrument, date=price_date.strftime('%Y-%m-%d'))
        update_fields = []
        for fieldPair in fieldMapping:
            field_name = re.sub('[^0-9a-zA-Z_]+', '_', fieldPair.datasource_field.name_c.lower())
            try:
                setattr(goldenRecordDB, fieldPair.goldenrecord_field.name_c.lower(), priceRecord[field_name])
                update_fields.append(fieldPair.goldenrecord_field.name_c.lower())
            except ValueError as e:
                pass
        
        if instrumentSyn.instrument.marketdatatype.id in [8,] and source == 'BBG': # if the instrument of type Future (Generic Future)
            goldenRecordDB, update_fields = update_future_golden_record(instrumentSyn, priceRecord, goldenRecordDB, price_date, update_fields, source)
        
        # update the timestamp of the current day
        if price_date.date() == datetime.now().date():
            setattr(goldenRecordDB, 'time_t', datetime.now().time())
            update_fields.append('time_t')
        if previous_price:
            if source == 'DS':
                goldenRecordDB.eod_log_return_n = price2LogRet(float(goldenRecordDB.eod_price_n), previous_price)
                update_fields.append('eod_log_return_n')
            elif source == 'BBG':
                goldenRecordDB.intra_log_return_n = price2LogRet(float(goldenRecordDB.intraday_price_n), previous_price)
                update_fields.extend(['intra_log_return_n'])
        # update golden record price record
        goldenRecordDB.save()
        
        if source == 'DS':
            return float(goldenRecordDB.eod_price_n)
        elif source == 'BBG':
            return float(goldenRecordDB.intraday_price_n)
    except ObjectDoesNotExist as e:
        try:
            # insert into golden record table 
            # populate golden record dictionary
            goldenRecord = {'instrument': instrumentSyn.instrument, 'date': price_date.strftime('%Y-%m-%d'), }
            # update the timestamp of the current day
            if price_date.date() == datetime.now().date():
                goldenRecord['time_t'] = datetime.now().time()
            for fieldPair in fieldMapping:
                field_name = re.sub('[^0-9a-zA-Z_]+', '_', fieldPair.datasource_field.name_c.lower())
                goldenRecord[fieldPair.goldenrecord_field.name_c.lower()] = priceRecord[field_name]
            if instrumentSyn.instrument.marketdatatype.id in [8,] and source == 'BBG': # if the instrument of type Future (Generic Future)
                goldenRecord = new_future_golden_record(instrumentSyn, goldenRecord, price_date, source)
            
            
            if previous_price:
                if source == 'DS':
                    goldenRecord['eod_log_return_n'] = price2LogRet(float(goldenRecord['eod_price_n']), previous_price)
                elif source == 'BBG':
                    goldenRecord['intra_log_return_n'] = price2LogRet(float(goldenRecord['intraday_price_n']), previous_price)
            
            goldenRecordDB = goldenRecordTable(**goldenRecord)
                
            goldenRecordDB.save(force_insert=True)
            if source == 'DS':
                return float(goldenRecordDB.eod_price_n)
            elif source == 'BBG':
                return float(goldenRecordDB.intraday_price_n)
        except Exception as e1:
            print("could not update or insert golden record data for this instrument:" + instrumentSyn.instrument.name_c + ",on this date:" + price_date.strftime('%Y-%m-%d'))
    except Exception as e:
        print('Error inserting new golden record' + instrumentSyn.instrument.name_c)
        
def insert_data(instrumentSyn, priceData, priceDataTable, goldenRecordTable, source):
    # select mapping
    fieldMapping = MarketDataField_Mapping.objects.filter(marketdatatype=instrumentSyn.instrument.marketdatatype, valid_to_d__isnull=True, datasource_field__data_source_c=source)
    previous_price = None
    for index, priceRecord in priceData.iterrows():
        priceRecord = priceRecord.to_dict()
        insert_source_price_record(instrumentSyn.instrument, priceRecord, priceDataTable, index)
        
        # try to insert golden records only if there is at least one existing field mapping
        if(len(fieldMapping) > 0):
            previous_price = insert_golden_record(instrumentSyn, priceRecord, goldenRecordTable, fieldMapping, index, source, previous_price)
