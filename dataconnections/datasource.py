'''
Created on 10.08.2016

@author: Moustafa Shama
'''
from pydatastream import Datastream
from _datetime import datetime,timedelta
import numpy as np
import re

def create_DataStreamConnection():
    return Datastream(username="DS:ZQAJ001", password="POINT954")

def get_metaData(instrument, datasource):
    if(datasource == 'DS'):
        instrumentFieldList = ['ISIN','NAME','MNEM','FLOT']
        DWE = create_DataStreamConnection()
        instrumentData = DWE.fetch(instrument, instrumentFieldList, static=True)
        bbName = instrumentData['MNEM'][0]
        shortName = instrumentData['MNEM'][0]
        description = instrumentData['NAME'][0]
        ISIN = instrumentData['ISIN'][0]
        try:
            vBPV = str(instrumentData['FLOT'][0])
            if(vBPV == 'NA'):
                vBPV = 0
        except Exception as e:
            vBPV = 0;
        return {'bbname':bbName,'shortname':shortName,'description':description,'ISIN':ISIN,'BPV':vBPV}
    elif(datasource == 'BBG'):
        print("note yet implemented")
        return
    
def get_PriceData(datasource, instrument, fields, lastPriceDate='2000-01-01'):
    lastPriceDate =  datetime.strptime(lastPriceDate, '%Y-%m-%d') - timedelta(days=5)
    if(datasource == 'DS'):
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