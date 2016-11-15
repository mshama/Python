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
from InstrumentDataManagement.models import Instrumentsynonym
from MarketDataManagement.models import MarketData_Fixed_Income_VW, MarketData_Derivative_VW, MarketData_InterestRate_VW, MarketData_Equity_VW, MarketData_Index_VW

def load_instrument(instrument):
    marketdatatype = Instrumentsynonym.objects.get(code_c=instrument).instrument.marketdatatype.type_c
    if marketdatatype == 'Equity':
        return load_equity_instrument(instrument)
    elif marketdatatype == 'Fixed_Income':
        return load_fixed_income_instrument(instrument)
    elif marketdatatype == 'InterestRate':
        return load_interestrate_instrument(instrument)
    elif marketdatatype == 'Derivative':
        return load_derivative_instrument(instrument)
    elif marketdatatype == 'Index':
        return load_index_instrument(instrument)

def load_equity_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Equity_VW.objects.filter(instrument=instrument).values()))
    del priceData['instrument_id']
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_fixed_income_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Fixed_Income_VW.objects.filter(instrument=instrument).defer('instrument_id').values()))
    del priceData['instrument_id']
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_derivative_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Derivative_VW.objects.filter(instrument=instrument).defer('instrument_id').values()))
    del priceData['instrument_id']
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_interestrate_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_InterestRate_VW.objects.filter(instrument=instrument).defer('instrument_id').values()))
    del priceData['instrument_id']
    
    instrumentData['priceData'] = priceData
    
    return instrumentData

def load_index_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Index_VW.objects.filter(instrument=instrument).defer('instrument_id').values()))
    del priceData['instrument_id']
    
    instrumentData['priceData'] = priceData
    
    return instrumentData