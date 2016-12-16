'''
Created on 30.09.2016

@author: Moustafa Shama

this file contains data loading functions that will be called from outside the quantserver scope
'''
import pandas as pd

# required to enable using django models outside of django APP
import django
import sys
import os



sys.path.append(os.path.abspath("../../QuantServer/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'QuantServer.settings'

django.setup()


# example remove afterwards to use be able to import this file
from InstrumentDataManagement.models import Instrumentsynonym, Instrument,\
    Marketdatatype, Market, Currency
from MarketDataManagement.models import MarketData_Fixed_Income_VW, MarketData_Derivative_VW, \
    MarketData_InterestRate_VW, MarketData_Equity_VW, MarketData_Index_VW,\
    MarketData_Currency_VW
from PortfolioPositionManagement.models import Investment


def get_instrument(ticker, marketdatatype, market=None, currency=None):
    '''
    checks if an instrument exists given the ticker
    
    @param ticker: ticker we want to check
    @param marketdatatype: the type of ticker (Equity, Index, ...etc)
    @param market: (optional) the market that the instrument should belong to
    @param currency: (optional) currency of the instrument
    
    @return: if instrument is found it returns the instrument and the investment if it is not found it returns the tuple (None, None)
    '''
    main_instrument = True
    if market != None:
        market = Market.objects.get(iso_code_c=market)
        main_instrument = False
        
    if currency != None:
        currency = Currency.objects.get(isocode_c=currency)
    
    marketdatatype = Marketdatatype.objects.get(name_c=marketdatatype)
    synonyms = Instrumentsynonym.objects.filter(code_c=ticker)
    for synonym in synonyms:
        if (synonym.instrument.marketdatatype == marketdatatype and
            synonym.instrument.main_instrument_b == main_instrument):
            if market != None:
                if synonym.instrument.market == market:
                    if synonym.instrument.currency == currency:
                        return synonym.instrument, Investment.objects.get(instrument=synonym.instrument)
                    else:
                        pass
                else:
                    pass
            else:
                if synonym.instrument.currency == currency:
                    return synonym.instrument, Investment.objects.get(instrument=synonym.instrument)
                else:
                    pass
    return None, None

def load_instrument_with_id(instrument_id, date_list=[], isrange=False):
    '''
    loads the instrument from database given its id and returns its price data
    
    @param instrument_id: database id of the instrument
    @param date_list: a list of dates or date range in string format YYYY-MM-DD
    @param isrange: marks the given data_list as a range so that we only use the first and second element of the list 
    
    @return: returns a list of dictionaries containing price data
    '''
    
    instrumentData = []
    
    marketdatatype = Instrument.objects.get(pk=instrument_id).marketdatatype.type_c
    current_instrument_data = {'instrumentName': Instrument.objects.get(pk=instrument_id).name_c}
    
    if marketdatatype == 'Equity':
        price_table = eval('MarketData_Equity_VW')
    elif marketdatatype == 'Fixed_Income':
        price_table = eval('MarketData_Fixed_Income_VW')
    elif marketdatatype == 'InterestRate':
        price_table = eval('MarketData_InterestRate_VW')
    elif marketdatatype == 'Derivative':
        price_table = eval('MarketData_Derivative_VW')
    elif marketdatatype == 'Index':
        price_table = eval('MarketData_Index_VW')
    elif marketdatatype == 'Currency':
        price_table = eval('MarketData_Currency_VW')
        
    if len(date_list) > 0:
        if isrange:
            price_data = price_table.objects.filter(
                                                    instrument__id=instrument_id, 
                                                    date__gte=date_list[0],
                                                    date__lte=date_list[1],
                                                    ).values().order_by('date')
            
        else:
            price_data = price_table.objects.filter(
                                                    instrument__id=instrument_id, 
                                                    date__in=date_list,
                                                    ).values().order_by('date')
    else:
        price_data = price_table.objects.filter(
                                                instrument__id=instrument_id,
                                                ).values().order_by('date')
    price_data = pd.DataFrame(list(price_data))
    del price_data['instrument_id']
    current_instrument_data['priceData'] = price_data
    
    instrumentData.append(current_instrument_data)

    return instrumentData

def load_instrument(instrument):
    '''
    reads price data from database given a ticker and returns it
    
    @param instrument: ticker can be DS Ticker, BBG Ticker or ISIN
    
    @return: list of dictionaries containing price data
    '''
    instrument_ids = Instrumentsynonym.objects.filter(code_c=instrument).values('instrument').exclude(validity_d__isnull=True).distinct()
    instrumentData = []
    for instrument_id in instrument_ids:
        marketdatatype = Instrument.objects.get(pk=instrument_id['instrument']).marketdatatype.type_c
        current_instrument_data = {'instrumentName': Instrument.objects.get(pk=instrument_id['instrument']).name_c}
        if marketdatatype == 'Equity':
            current_instrument_data['priceData'] = load_equity_instrument(instrument_id['instrument'])
        elif marketdatatype == 'Fixed_Income':
            current_instrument_data['priceData'] = load_fixed_income_instrument(instrument_id['instrument'])
        elif marketdatatype == 'InterestRate':
            current_instrument_data['priceData'] = load_interestrate_instrument(instrument_id['instrument'])
        elif marketdatatype == 'Derivative':
            current_instrument_data['priceData'] = load_derivative_instrument(instrument_id['instrument'])
        elif marketdatatype == 'Index':
            current_instrument_data['priceData'] = load_index_instrument(instrument_id['instrument'])
        elif marketdatatype == 'Currency':
            current_instrument_data['priceData'] = load_currency_instrument(instrument_id['instrument'])
        instrumentData.append(current_instrument_data)
        
    return instrumentData

def load_equity_instrument(instrument_id):
    
    priceData = pd.DataFrame(list(MarketData_Equity_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id']    
    
    return priceData


def load_fixed_income_instrument(instrument_id):
    priceData = pd.DataFrame(list(MarketData_Fixed_Income_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id']
    
    return priceData

def load_derivative_instrument(instrument_id):
    priceData = pd.DataFrame(list(MarketData_Derivative_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id'] 
    
    return priceData


def load_interestrate_instrument(instrument_id):
    priceData = pd.DataFrame(list(MarketData_InterestRate_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id'] 
    
    return priceData

def load_index_instrument(instrument_id):
    priceData = pd.DataFrame(list(MarketData_Index_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id']
     
    return priceData

def load_currency_instrument(instrument_id):
    priceData = pd.DataFrame(list(MarketData_Currency_VW.objects.filter(instrument__id=instrument_id).values().order_by('date')))
    del priceData['instrument_id']
    
    return priceData
