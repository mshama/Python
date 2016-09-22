from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.db.models import Max
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# build in libraries
import pandas as pd
from _datetime import datetime

# own libraries
from dataconnections.datasource import get_metaData, get_PriceData

# models import
from .models import Instrument, Instrumentsynonym, Codification

# forms import
from .forms import newMarketDataTypeForm,newMarketForm,newInstrumentForm, newCountryForm, newCurrencyForm

# Create your views here.

def index(request):
    context = {'message': 'this is the data management home'}
    return render(request, 'InstrumentDataManagement/index.html', context)

def viewInstrument(request):
    if request.method == 'POST':
        print()
    elif request.method == 'GET':
        print()
        
def newInstrument(request):
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
    form = newInstrumentForm(request.POST)
    if form.is_valid():
        if form.cleaned_data['codification'].name_c in ['ISIN', 'DS_Ticker']:
            source = 'DS'
            ticker = 'DS_Ticker'
        else:
            source = 'BBG'
            ticker = 'BBG_Ticker'
        instrumentCodes = form.cleaned_data['names'].split('\r\n')
        for instrumentCode in instrumentCodes:
            instrument_metaData = get_metaData(instrumentCode, source)
            instrument = Instrument(
                            name_c = instrument_metaData['name'],
                            market = form.cleaned_data['market'],
                            marketdatatype = form.cleaned_data['marketdatatype'],
                            country = form.cleaned_data['country'],
                            risk_country = form.cleaned_data['risk_country'],
                            currency = form.cleaned_data['currency'], 
                            underlying_currency = form.cleaned_data['underlyingcurrency'],
                            bpv_n = instrument_metaData['BPV'],
                        )
            instrument.save()
            # save ticker mapping
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.filter(name_c=ticker)[0],
                code_c = instrument_metaData['ticker'],
                validity_d = datetime.now().date(),
            ).save()
            # save isin 
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.filter(name_c='ISIN')[0],
                code_c = instrument_metaData['ISIN'],
                validity_d = datetime.now().date(),
            ).save()

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
    