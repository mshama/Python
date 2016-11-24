'''
Created on 10.08.2016

@author: Moustafa Shama
'''
from pydatastream import Datastream
from _datetime import datetime,timedelta
import numpy as np
import re
import pycountry
import pandas as pd

def create_DataStreamConnection():
    return Datastream(username="DS:ZQAJ001", password="POINT954")

def remove_invalid(data, fields):
    """
    this function takes a dictionary and removes invalid values like 'NA' and replace them with None
    if one of the fields doesn't exist it adds it with None value
    input:
        data: dictionary containing the data that need to be cleaned
        fields: list of fields that should be existing in the dictionary
    output:
        data: after cleaning
    """
    for field in fields:
        try:
            field_value = str(data[field][0])
            if(field_value == 'NA'):
                field_value = None
                data[field][0] = field_value
        except Exception as e:
            data[field][0] = None
    return data

def get_metaData_DS(instrument):
    instrumentFieldList = ['ISIN','NAME','MNEM','FLOT','DSCD', 'OS']
    DWE = create_DataStreamConnection()
    try:
        instrumentData = DWE.fetch(instrument, instrumentFieldList, static=True)
        ticker = str(instrumentData['MNEM'][0])
        name = str(instrumentData['NAME'][0])
        ISIN = str(instrumentData['ISIN'][0])
        code = str(instrumentData['DSCD'][0])
        try:
            vBPV = str(instrumentData['FLOT'][0])
            if(vBPV == 'NA'):
                vBPV = None
        except Exception as e:
            vBPV = None
        try:
            strike = instrumentData['OS'][0]
            if(strike == 'NA'):
                strike = None
        except Exception as e:
            strike = None
    except TypeError:
        ticker = None
        name = None
        ISIN = None
        code = None
        vBPV = None
        strike = None
    finally:
        return {
                'DS_Ticker':ticker,
                'name':name,
                'ISIN':ISIN,
                'BPV':vBPV,
                'DS_Code':code,
                'country': None,
                'cntry_of_risk': None,
                'strike': strike,
                'expiry_date':None,
                }
    
def get_main_market_field(instrument_type):
    """
    this function returns the main market (Hauptbörse) Bloomberg field given instrument type 
    """
    return {
            'Equity':       'EQY_PRIM_SECURITY_PRIM_EXCH',
            'Fixed_Income': 'PRICING_SOURCE',
            'Derivative':   'ID_MIC_PRIM_EXCH',
            }.get(instrument_type)
            
def get_static_BBG(instrument_ticker, fields=[]):
    from xmlrpc import client
        
    proxy = client.ServerProxy('http://192.168.100.20:8080')
    try:
        static_data = proxy.get_reference_data(instrument_ticker, fields)
        # remove ticker field
        static_data.pop('ticker')
        # remove non valid values 'NULL' and replace them with None
        for key, value in static_data.items():
            static_data[key] = [item if item != 'NULL' else None for item in value]
        return static_data
    except TimeoutError:
        print('connection to BBG server cannot be established. make sure that the RPC service is running')
        return None
    except Exception as e:
        pass
    return {}

def get_metaData_ISIN(ISIN, instrument_type, market=None):
    """
    - this function searches in Bloomberg for the main ticker given an ISIN and then returns data using get_metaData_BBG.
      if ISIN is None it returns empty data
    - inputs:
        ISIN: a 12 character instrument identification.
        instrument_type: the main classification for the instrument (Equity, Derivative, ..etc)
        market: is an optional value to specifically search for a ticker in a certain market 
    """
    # if ISIN is None then there is no data to search for in Bloomberg so return empty data
    if ISIN == None:
        return {'BBG_Ticker':None,
                'name':None,
                'ISIN':None,
                'BPV':None,
                'country': None,
                'cntry_of_risk': None,
                'strike': None,
                'expiry_date':None,
                'market': None,
                }
    # establish connection to the rpc server
    from xmlrpc import client
    proxy = client.ServerProxy('http://192.168.100.20:8080')
    # read the list of instruments that belongs to this ISIN
    try:
        ticker_list = proxy.get_securities(ISIN)
        if len(ticker_list) > 1:
            # if we have more than one instrument then we have to find the one that corresponds to the main market
            if instrument_type == 'Derivative':
                # if it is a Derivative then we select the first Generic ticker
                main_ticker_desc = [ticker for ticker in ticker_list['description'] if 'Generic 1st' in ticker][0]
                main_ticker = ticker_list['security'][ticker_list['description'].index(main_ticker_desc)]
            elif market == None and instrument_type != 'Derivative':
                # get the the main market using the first ticker
                main_market_field = get_main_market_field(instrument_type)
                main_market = proxy.get_bloomberg_instr_meta_data(ticker_list['security'][0],[main_market_field])
                # search in the list of tickers for the one with the same main market code
                main_ticker = [ticker for ticker in ticker_list['security'] if ' '+main_market[main_market_field]+' ' in ticker][0]
            else:
                main_ticker = [ticker for ticker in ticker_list['security'] if ' '+market+' ' in ticker][0]
            # read meta data for this ticker and return it
            return get_metaData_BBG(main_ticker,instrument_type)
        else:
            return get_metaData_BBG(ticker_list['security'][0],instrument_type)
    except TimeoutError:
        print('connection to BBG server cannot be established. make sure that the RPC service is running')
        return None

def get_metaData_BBG(instrument,instrument_type):
    instrument_data = None
    try:
        from xmlrpc import client
        proxy = client.ServerProxy('http://192.168.100.20:8080')
        main_market_field = get_main_market_field(instrument_type)
        fields = ['NAME', 'ID_ISIN', 'CNTRY_OF_RISK', 'COUNTRY_ISO', 'FUT_CONT_SIZE', 'OPT_STRIKE_PX']
        if main_market_field:
            fields.append(main_market_field)
        instrument_data = proxy.get_bloomberg_instr_meta_data(instrument, fields)
        
        instrument_data =  {'BBG_Ticker':str(instrument_data['ticker']),
                            'name':str(instrument_data['NAME']),
                            'ISIN':str(instrument_data['ID_ISIN']),
                            'BPV':instrument_data['FUT_CONT_SIZE'],
                            'country': str(pycountry.countries.get(alpha_2=instrument_data['COUNTRY_ISO']).alpha_3) if instrument_data['COUNTRY_ISO']!='NULL' else None,
                            'cntry_of_risk': str(pycountry.countries.get(alpha_2=instrument_data['CNTRY_OF_RISK']).alpha_3) if instrument_data['CNTRY_OF_RISK']!='NULL' else None,
                            'strike': str(instrument_data['OPT_STRIKE_PX']),
                            'expiry_date':None,
                            'market': str(instrument_data[main_market_field]) if main_market_field else None,
                            }
        
        for key, value in instrument_data.items():
            instrument_data[key] = value if value != 'NULL' else None
    except TimeoutError:
        print('connection to BBG server cannot be established. make sure that the RPC service is running')
        return None
    except Exception as e:
        print('an error while reading data:' + e)
        instrument_data =  {'BBG_Ticker':None,
                            'name':None,
                            'ISIN':None,
                            'BPV':None,
                            'country': None,
                            'cntry_of_risk': None,
                            'strike': None,
                            'expiry_date':None,
                            'market': None,
                            }
    finally:
        return instrument_data
    
def get_metaData(instrument, datasource, instrument_type=''):
    if(datasource == 'DS'):
        return get_metaData_DS(instrument)
    elif(datasource == 'BBG'):
        return get_metaData_BBG(instrument,instrument_type)

def get_bond_metaData(instrument):
    instrumentFieldList = ['NOMV', 'LF', 'AMOR', 'RD','BTYP','C', 'FRC','FRM',]
    DWE = create_DataStreamConnection()
    try:
        instrumentData = DWE.fetch(instrument, instrumentFieldList, static=True)
        
        instrumentData = remove_invalid(instrumentData, instrumentFieldList)
    
        return {
                'nominal':instrumentData['NOMV'][0],
                'life':instrumentData['LF'][0], 
                'amortisation_type':instrumentData['AMOR'][0], 
                'redemption':instrumentData['BTYP'][0],
                'bond_type':instrumentData['BTYP'][0],
                'coupon_current':instrumentData['C'][0], 
                'coupon_floating':instrumentData['FRC'][0], 
                'floating_real_margin':instrumentData['FRM'][0],
                }
    except Exception:
        return {
                'nominal':None,
                'life':None, 
                'amortisation_type':None, 
                'redemption':None,
                'bond_type':None,
                'coupon_current':None, 
                'coupon_floating':None, 
                'floating_real_margin':None,
                }

def get_DS_PriceData(instrument, fields, lastPriceDate):
    DWE = create_DataStreamConnection();
    try:
        priceData = DWE.fetch(instrument,
                                  fields=fields[0] + '#S', #to filter the holidays
                                  date_from=lastPriceDate.strftime('%Y-%m-%d'), 
                                  #date_to=datetime.today().strftime('%Y-%m-%d') # include date_to if we want the data to be till current day. remove it if we only want the data till the current actual available date from DataStream
                                )
        priceData.columns = [fields[0].lower()]
    except Exception as e:
        priceData = DWE.fetch(instrument,
                                  fields=fields[0], #to filter the holidays
                                  date_from=lastPriceDate.strftime('%Y-%m-%d'), 
                                  #date_to=datetime.today().strftime('%Y-%m-%d') # include date_to if we want the data to be till current day. remove it if we only want the data till the current actual available date from DataStream
                                )
    i = 1;     
    for field in fields[1:]:
        try:
            tempPriceData = DWE.fetch(instrument,
                                      fields=field + '#S', #to filter the holidays
                                      date_from=lastPriceDate.strftime('%Y-%m-%d'), 
                                      #date_to=datetime.today().strftime('%Y-%m-%d') # include date_to if we want the data to be till current day. remove it if we only want the data till the current actual available date from DataStream
                                    )
            tempPriceData.columns = [field.lower()]
        except Exception as e:
            tempPriceData = DWE.fetch(instrument,
                                      fields=field, #to filter the holidays
                                      date_from=lastPriceDate.strftime('%Y-%m-%d'), 
                                      #date_to=datetime.today().strftime('%Y-%m-%d') # include date_to if we want the data to be till current day. remove it if we only want the data till the current actual available date from DataStream
                                    )
        i = i + 1;
                  
        priceData = priceData.join(tempPriceData) #pd.merge(priceData, tempPriceData, on='Date', how='outer',suffixes=['', ''])
        del tempPriceData
    priceData = priceData.dropna(axis=0, how = 'any'); # drop rows with all NA values
    priceData[np.isnan(priceData)] = 'NULL' # convert NA values to NULL to be inserted correctly in the database
    fieldnames = [re.sub('[^0-9a-zA-Z_]+', '_', field.lower()) for field in priceData.keys()] # make sure that all fields are in small letters
    priceData.columns = fieldnames
    return priceData

def get_BBG_PriceData(instrument, fields, lastPriceDate, end_date = datetime.now()):
    from xmlrpc import client
        
    proxy = client.ServerProxy('http://192.168.100.20:8080')
    try:
        price_data = proxy.get_historical_data(instrument, fields, lastPriceDate.strftime('%Y%m%d'), end_date.strftime("%Y%m%d"))
        # check if data was empty then try to read current data
        if not price_data:
            price_data = proxy.get_reference_data(instrument, fields)
        # remove ticker field
        price_data.pop('ticker')
        # remove non valid values 'NULL' and replace them with None
        for key, value in price_data.items():
            price_data[key] = [item if item != 'NULL' else None for item in value]
        # convert the date column from type string to type datetime
        for i in range(len(price_data['date'])):
            price_data['date'][i] = datetime.strptime(price_data['date'][i],'%Y-%m-%d')
        # convert the dictionary to a dataframe with index to be the date column
        price_data = pd.DataFrame.from_dict(price_data).set_index('date')
        # converts keys to lower case to match the field names of the model class
        fieldnames = [field.lower() for field in price_data.keys()]
        price_data.columns = fieldnames
        return price_data
    except TimeoutError:
        print('connection to BBG server cannot be established. make sure that the RPC service is running')
        return None
    except Exception as e:
        pass
    return None

def get_PriceData(datasource, instrument, fields, lastPriceDate='2000-01-01'):
    lastPriceDate =  datetime.strptime(lastPriceDate, '%Y-%m-%d') - timedelta(days=5)
    if(datasource == 'DS'):
        return get_DS_PriceData(instrument, fields, lastPriceDate)
    elif(datasource == 'BBG'):
        return get_BBG_PriceData(instrument, fields, lastPriceDate)
        