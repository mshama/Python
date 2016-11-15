from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseNotFound
from django.db.models import Max
from django.db.models import Q
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

# build in libraries
import pandas as pd
from _datetime import datetime
import pycountry

# own libraries
from dataconnections.datasource import get_metaData, get_bond_metaData,\
    get_metaData_ISIN

# models import
from .models import Instrument, Instrumentsynonym, Country, Codification,\
    AssetClass, AssetClass_Instrument, Bond, Market

# forms import
from .forms import newMarketDataTypeForm,newMarketForm,newInstrumentForm,\
    newCountryForm, newCurrencyForm, newAssetClassForm, instrumentAssetClassMapping, newInstrumentSynonymForm

# Create your views here.

def index(request):
    context = {'message': 'this is the data management home'}
    return render(request, 'InstrumentDataManagement/index.html', context)

def addInstrumentSynonym(request):
    form = newInstrumentSynonymForm(request.POST)
    if form.is_valid():
        try:
            instrument = Instrument.objects.get(pk=form.cleaned_data['instrument'])
            Instrumentsynonym(instrument=instrument,
                              codification=form.cleaned_data['codification'],
                              code_c = form.cleaned_data['code_c'],
                              validity_d = datetime.now().date()).save()
        except IntegrityError as e:
            msg = "Cannon Insert this Synonym. Either it already exists or the Instrument has already a Synonym with the same type"
        return redirect('InstrumentDataManagement:viewInstrument',instrument_id=instrument.id, msg=msg)
    return redirect('InstrumentDataManagement:viewInstrument')

def deltInstrumentSynonym(request, synonym_id):
    synonym = Instrumentsynonym.objects.get(pk=synonym_id)
    instrument_id = synonym.instrument.id
    synonym.delete()
    
    return redirect('InstrumentDataManagement:viewInstrument', instrument_id=instrument_id, )

def viewInstrument(request, instrument_id='', msg=None):
    if request.method == 'POST':
        print()
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
            # first read the meta data 
            if form.cleaned_data['source'] == 'DS':
                instrument_metaData_DS = get_metaData(instrumentCode, form.cleaned_data['source'])
                instrument_metaData_BBG = get_metaData_ISIN(instrument_metaData_DS['ISIN'], form.cleaned_data['marketdatatype'].type_c, market)
                try:
                    # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                    inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                    if inst_syn.instrument.marketdatatype.name_c == form.cleaned_data['marketdatatype'].name_c:
                        return
                except ObjectDoesNotExist as e:
                    pass
            elif form.cleaned_data['source'] == 'BBG':
                try:
                    # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                    Instrumentsynonym.objects.get(code_c=instrumentCode)
                    return
                except ObjectDoesNotExist as e:
                    # otherwise read the meta data from bloomberg and datastream
                    instrument_metaData_BBG = get_metaData(instrumentCode, form.cleaned_data['source'], form.cleaned_data['marketdatatype'].type_c)
                    instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
            elif form.cleaned_data['source'] == 'ISIN':
                instrument_metaData_BBG = get_metaData_ISIN(instrumentCode,form.cleaned_data['marketdatatype'].type_c, market)
                try:
                    # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                    inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                    if inst_syn.instrument.marketdatatype.name_c == form.cleaned_data['marketdatatype'].name_c:
                        return
                except ObjectDoesNotExist as e:
                    instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
            try:
                # try to select market data based on the value from BBG meta data if there was no manually specified market
                market = form.cleaned_data['market']
                if instrument_metaData_BBG['market'] != None and market == None:
                    market = Market.objects.get(
                                    iso_code_c= instrument_metaData_BBG['market']
                                    )
            except ObjectDoesNotExist:
                # if the market doesn't exist then create it
                market = Market(
                                iso_code_c = instrument_metaData_BBG['market'],
                                name_c = instrument_metaData_BBG['market'],
                            )
                market.save()
            try:
                country = form.cleaned_data['country']
                if instrument_metaData_BBG['country'] != None and country == None:
                    country = Country.objects.get(isocode_c=instrument_metaData_BBG['country'])
            except ObjectDoesNotExist:
                country = Country(
                                  isocode_c = instrument_metaData_BBG['country'],
                                  name_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['country']).name,
                                  denomination_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['country']).official_name
                                  )
                country.save()
            
            try:
                risk_country = form.cleaned_data['risk_country']
                if instrument_metaData_BBG['cntry_of_risk'] != None and risk_country == None:
                    risk_country = Country.objects.get(isocode_c=instrument_metaData_BBG['cntry_of_risk'])
            except ObjectDoesNotExist:
                risk_country = Country(
                                  isocode_c = instrument_metaData_BBG['cntry_of_risk'],
                                  name_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['cntry_of_risk']).name,
                                  denomination_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['cntry_of_risk']).official_name
                                  )
                risk_country.save()
            try:
                # try to create a new instrument
                instrument = Instrument(
                                        name_c = instrument_metaData_BBG['name'] if instrument_metaData_BBG['name']!=None else instrument_metaData_DS['name'],
                                        market = market,
                                        marketdatatype = form.cleaned_data['marketdatatype'],
                                        country = country,
                                        risk_country = risk_country,
                                        currency = form.cleaned_data['currency'], 
                                        underlying_currency = form.cleaned_data['underlyingcurrency'],
                                        bpv_n = float(instrument_metaData_BBG['BPV']),
                                    )
                instrument.save()
                # if the instrument is with type bond we need to read extra data for it
                if (instrument.marketdatatype.name_c == 'Bonds'):
                    bond_meta_data = get_bond_metaData(instrument_metaData_DS['ISIN'])
                    Bond(
                        instrument = instrument,
                        nominal_n = bond_meta_data['nominal'],
                        life_n = bond_meta_data['life'],
                        coupon_current_n = bond_meta_data['coupon_current'],
                        coupon_floating_n = bond_meta_data['coupon_floating'],
                        floating_real_margin_n = bond_meta_data['floating_real_margin'],
                        amortisationtype_c = bond_meta_data['amortisation_type'],
                        bondtype_c = bond_meta_data['bond_type'],
                        ).save()
                # insert the synonyms for the current instrument
                if instrument_metaData_DS['DS_Ticker'] != 'NA':
                    Instrumentsynonym(
                        instrument = instrument,
                        codification = Codification.objects.get(name_c='DS_Ticker'),
                        code_c = instrument_metaData_DS['DS_Ticker'],
                        validity_d = datetime.now().date(),
                    ).save()
                if instrument_metaData_DS['DS_Code'] != 'NA':
                    Instrumentsynonym(
                        instrument = instrument,
                        codification = Codification.objects.get(name_c='DS_Code'),
                        code_c = instrument_metaData_DS['DS_Code'],
                        validity_d = datetime.now().date(),
                    ).save()
                if instrument_metaData_BBG['BBG_Ticker'] != None:
                    Instrumentsynonym(
                        instrument = instrument,
                        codification = Codification.objects.get(name_c='BBG_Ticker'),
                        code_c = instrument_metaData_BBG['BBG_Ticker'],
                        validity_d = datetime.now().date(),
                    ).save()
                if instrument_metaData_BBG['ISIN'] != None:
                    Instrumentsynonym(
                        instrument = instrument,
                        codification = Codification.objects.filter(name_c='ISIN')[0],
                        code_c = instrument_metaData_BBG['ISIN'],
                        validity_d = datetime.now().date(),
                    ).save()
            except Exception as e:
                ## we need to collect instruments with errors and send an email containing the errors faced
                ## during the insertion
                pass

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