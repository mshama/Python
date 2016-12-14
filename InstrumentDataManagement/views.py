from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db import IntegrityError

# build in libraries
from datetime import datetime

# models import
from .models import Instrument, Instrumentsynonym, \
    AssetClass, AssetClass_Instrument

# forms import
from .forms import newMarketDataTypeForm,newMarketForm,newInstrumentForm,\
    newCountryForm, newCurrencyForm, newAssetClassForm, instrumentAssetClassMapping, newInstrumentSynonymForm


from data_saving.saving_functions import new_instrument
from MarketDataManagement.models import MarketData_Equity_DataStream_C,\
    MarketData_Equity_Bloomberg_C, MarketData_Equity_C,\
    MarketData_Fixed_Income_DataStream_C, MarketData_Fixed_Income_Bloomberg_C,\
    MarketData_InterestRate_DataStream_C, MarketData_InterestRate_Bloomberg_C,\
    MarketData_Derivative_DataStream_C, MarketData_Derivative_Bloomberg_C,\
    MarketData_Index_DataStream_C, MarketData_Index_Bloomberg_C,\
    MarketData_Derivative_C, MarketData_InterestRate_C,\
    MarketData_Fixed_Income_C, MarketData_Index_C
from InstrumentDataManagement.models import Codification
from InstrumentDataManagement.forms import instrumentSearchForm

# Create your views here.

def index(request):
    context = {'message': 'this is the data management home'}
    return render(request, 'InstrumentDataManagement/index.html', context)

def searchInstruments(request):
    if request.method == 'GET':
        searchForm = instrumentSearchForm()
        context = {
                   'searchForm': searchForm
                   }
        return render(request, 'InstrumentDataManagement/searchInstruments.html', context)
    elif request.method == 'POST':
        searchForm = instrumentSearchForm(request.POST)
        if searchForm.is_valid():
            instrumentCodes = searchForm.cleaned_data['names'].split('\r\n')
            if searchForm.cleaned_data['source'] == 'DS':
                ticker_type = 'DS_Ticker'
            elif searchForm.cleaned_data['source'] == 'BBG':
                ticker_type = 'BBG_Ticker'
            elif searchForm.cleaned_data['source'] == 'ISIN':
                ticker_type = 'ISIN'
                
            instruments = Instrument.objects.filter(instrumentsynonym__code_c__in=instrumentCodes, instrumentsynonym__codification=Codification.objects.get(name_c=ticker_type))
            
            if searchForm.cleaned_data['marketdatatype']:
                instruments = [i for i in instruments if i.marketdatatype == searchForm.cleaned_data['marketdatatype']]
                
            if searchForm.cleaned_data['market']:
                instruments = [i for i in instruments if i.marketdatatype == searchForm.cleaned_data['market']]
        
        else:
            instruments = []
        
        context = {
                   'instruments': instruments,
                   }
        return render(request, 'InstrumentDataManagement/viewInstruments.html', context)

def addInstrumentSynonym(request):
    form = newInstrumentSynonymForm(request.POST)
    if form.is_valid():
        try:
            instrument = Instrument.objects.get(pk=form.cleaned_data['instrument'])
            Instrumentsynonym(instrument=instrument,
                              codification=form.cleaned_data['codification'],
                              code_c = form.cleaned_data['code_c'],
                              validity_d = datetime.now().date()).save()
        except IntegrityError:
            msg = "Cannon Insert this Synonym. Either it already exists or the Instrument has already a Synonym with the same type"
        return redirect('InstrumentDataManagement:viewInstrument',instrument_id=instrument.id, msg=msg)
    return redirect('InstrumentDataManagement:viewInstrument')

def deltInstrumentSynonym(request, synonym_id):
    synonym = Instrumentsynonym.objects.get(pk=synonym_id)
    instrument_id = synonym.instrument.id
    synonym.delete()
    
    return redirect('InstrumentDataManagement:viewInstrument', instrument_id=instrument_id, )

def deleteInstrument(request, instrument_id=None):
    if instrument_id != None:
        instrument = Instrument.objects.get(pk=instrument_id)
        
        instrument.delete()
        
        return redirect('InstrumentDataManagement:viewInstrument')
    

def viewInstrument(request, instrument_id='', msg=None):
    if request.method == 'POST':
        pass
    elif request.method == 'GET':
        if instrument_id != '':
            instrumentSynonyms = Instrumentsynonym.objects.filter(instrument_id=instrument_id).order_by('codification')
            instrument = Instrument.objects.get(id=instrument_id)
            synonymForm = newInstrumentSynonymForm(initial={'instrument': instrument_id})
            context = {
                       'instrumentSynonyms': instrumentSynonyms,
                       'instrument': instrument,
                       'synonymForm': synonymForm,
                       'errorMessages': msg,
                       }
            return render(request, 'InstrumentDataManagement/viewInstrumentDetails.html', context)
        else:
            instruments = Instrument.objects.all()
        
            context = {
                       'instruments': instruments,
                       }
            return render(request, 'InstrumentDataManagement/viewInstruments.html', context)
        
def newInstrument(request):
    # check which type of post was executed in the html
    if request.method == 'POST':
        if 'newInstrument' in request.POST:
            insertInstruments(request)                    
        elif 'newMarketDataType' in request.POST:
            newMarketDataType(request)
        elif 'newMarket' in request.POST:
            newMarket(request)
        elif 'newCountry' in request.POST:
            newCountry(request)
        elif 'newCurrency' in request.POST:
            newCurrency(request)
    instrumentForm = newInstrumentForm()
    marketDataTypeForm = newMarketDataTypeForm()
    marketForm = newMarketForm()
    countryForm = newCountryForm()
    currencyForm = newCurrencyForm()
    
    context = {
               'message': 'this is the data management home',
               'instrumentForm': instrumentForm,
               'marketDataTypeForm': marketDataTypeForm,
               'marketForm': marketForm,
               'countryForm': countryForm,
               'currencyForm': currencyForm,
               }
    return render(request, 'InstrumentDataManagement/newInstrument.html', context)

def insertInstruments(request):
    """
    when a new instrument is inserted from the UI we don't check if it already exists
    we try to read the meta data for it and insert it as a new instrument
    """
    
    form = newInstrumentForm(request.POST)
    if form.is_valid():
        instrumentCodes = form.cleaned_data['names'].split('\r\n')
        market = form.cleaned_data['market'].iso_code_c if form.cleaned_data['market'] != None else None
        for instrumentCode in instrumentCodes:
            new_instrument(instrument_ticker=instrumentCode, 
                           ticker_type=form.cleaned_data['source'], 
                           market_data_type=form.cleaned_data['marketdatatype'].name_c, 
                           currency=form.cleaned_data['currency'], 
                           underlying_curreny=form.cleaned_data['underlyingcurrency'], 
                           market=form.cleaned_data['market'],
                           country=form.cleaned_data['country'],
                           risk_country=form.cleaned_data['risk_country'])

def newMarketDataType(request):
    form = newMarketDataTypeForm(request.POST)
    if not form.save():
        return False
        
def newMarket(request):
    form = newMarketForm(request.POST)
    if not form.save():
        return False
        
def newCountry(request):
    form = newCountryForm(request.POST)
    if not form.save():
        return False

def newCurrency(request):
    form = newCurrencyForm(request.POST)
    if not form.save():
        return False
        
def viewAssetClasses(request, assetclass_id=''):
    if request.method == 'GET':
        if assetclass_id != '':
            asset_class = AssetClass.objects.get(pk=assetclass_id)
            mappings = AssetClass_Instrument.objects.filter(assetclass=asset_class)
            mappingForm = instrumentAssetClassMapping()
            context = {                       
                       'asset_class': asset_class,
                       'mappings': mappings,
                       'mappingForm': mappingForm,
                       }
            return render(request, 'InstrumentDataManagement/viewAssetClassDetails.html', context)
        else:
            asset_classes = AssetClass.objects.all().order_by('parent_assetclass')
            assetClassForm = newAssetClassForm()
            context = {
                       'asset_classes': asset_classes,
                       'assetClassForm': assetClassForm,
                       }
            return render(request, 'InstrumentDataManagement/viewAssetClasses.html', context)
        
def newAssetClass(request):
    if request.method == 'POST':
        form = newAssetClassForm(request.POST)
        if form.is_valid():
            asset_class = AssetClass(**form.cleaned_data)
            if asset_class.parent_assetclass is None:
                asset_class.level_n = 0
            else:
                asset_class.level_n = asset_class.parent_assetclass.level_n + 1
            asset_class.save()
            return redirect('InstrumentDataManagement:viewAssetClasses')
        else:
            return HttpResponse('Error')

def deltInstrumentAssetClass(request, assetclass_id=''):
    if request.method == 'POST':
        mappings_ids = request.POST.getlist('mappings_ids')
        mapings = AssetClass_Instrument.objects.filter(pk__in=mappings_ids).delete()
        return redirect('InstrumentDataManagement:viewAssetClasses', assetclass_id=assetclass_id, )
        
def addInstrumentAssetClass(request, assetclass_id=''):
    if request.method == 'POST':
        mappingForm = instrumentAssetClassMapping(request.POST)
        if mappingForm.is_valid():
            asset_class = AssetClass.objects.get(pk=assetclass_id)
            for instrument in mappingForm.cleaned_data['instruments']:
                AssetClass_Instrument(assetclass=asset_class,
                                      instrument=instrument,
                                      mandate=mappingForm.cleaned_data['mandate']).save()
            return redirect('InstrumentDataManagement:viewAssetClasses', assetclass_id=assetclass_id, )