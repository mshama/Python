'''
Created on 30.09.2016

@author: Moustafa Shama
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
from MarketDataManagement.models import MarketData_Bond_C, MarketData_Derivative_C, MarketData_InterestRate_C, MarketData_Stock_C 


def load_stock_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Stock_C.objects.filter(instrument=instrument).defer('instrument_id').values()))
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_bond_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Stock_C.objects.filter(instrument=instrument).defer('instrument_id').values()))
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_derivative_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Stock_C.objects.filter(instrument=instrument).defer('instrument_id').values()))
    
    instrumentData['priceData'] = priceData
    
    return instrumentData


def load_interestrate_instrument(instrument):
    instrumentData = {'instrumentName': instrument}
    instrument = Instrumentsynonym.objects.get(code_c=instrument).instrument
    
    priceData = pd.DataFrame(list(MarketData_Stock_C.objects.filter(instrument=instrument).defer('instrument_id').values()))
    
    instrumentData['priceData'] = priceData
    
    return instrumentData