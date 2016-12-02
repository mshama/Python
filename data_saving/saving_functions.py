'''
Created on 30.09.2016

@author: Moustafa Shama

this file contains the saving functions that will be used outside of quantserver scope
'''
import pandas as pd
import pycountry


# required to enable using django models outside of django APP
import django
import sys
import os
from matplotlib import ticker


from django.core.exceptions import ObjectDoesNotExist
from misc.email import send_email


sys.path.append(os.path.abspath("../../QuantServer/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'QuantServer.settings'

django.setup()

from datetime import datetime

from InstrumentDataManagement.models import Marketdatatype, Instrumentsynonym, Instrument, Currency, \
                                            Country, Bond, Market, Codification
from PortfolioPositionManagement.models import Transaction, Portfolio, Position,\
    Investment
    

from dataconnections.datasource import get_metaData, get_bond_metaData, get_metaData_ISIN

from data_loading.loading_functions import get_instrument

def prepare_data(input_data):
    if 'isin' in input_data:
        field = 'isin'
    elif 'bbg' in input_data:
        field = 'bbg'
    elif 'ds' in input_data:
        field = 'ds'
    elif 'cash' in input_data:
        field = 'cash'
    else:
        return None
    
    _, investment = get_instrument(input_data[field], input_data['market_data_type_c'])
    if investment == None:
        currency = Currency.objects.get(pk=input_data['currency_id'])
        if field == 'cash':
            _, investment = new_cash_instrument(input_data[field], currency)
        else:
            _, investment = new_instrument(instrument_ticker=input_data[field], 
                                           ticker_type=field.upper(), 
                                           market_data_type=input_data['market_data_type_c'], 
                                           currency=currency)
    input_data['investment_id'] = investment.id
    
    del input_data[field]
    del input_data['market_data_type_c']
    
    return input_data
    

def save_in_DB(input_data, table_name, with_instrument=False):
    """
    this function is a generic function to save data directly in the database for quick data filling
    
    @param input_data: a pandas dataframe containing the data to be saved. column names must be same as the table column names
    @param table_name: destination table of the data
    @param with_instrument: specify if the incoming data contain information about the instrument instead of instrument_id 
    
    @return: returns list of error messages faced during insertion/update
    """
    # get class object of the corresponding table
    db_table = eval(table_name)
    errors = []
    # make sure that all fields are in small letters
    fieldnames = [field.lower() for field in input_data.keys()] 
    input_data.columns = fieldnames
    try:
        for index, record in input_data.iterrows():
            try:
                # convert to dictionary
                new_record = record.to_dict()
                if with_instrument:
                    new_record = prepare_data(new_record)
                # create a new database object
                new_record = db_table(**new_record)
                # save database object
                new_record.save()
            except Exception as e:
                errors.append(e)
    except Exception:
        pass
    return errors

def new_cash_instrument(instrument_ticker, currency=None, active=True):
    '''
    
    @param instrument_ticker: cash ticker
    @param currency:
    @param active:
    '''
    
    codification = Codification.objects.get(name_c='Internal')
    try:
        instrument = Instrumentsynonym.objects.get(code_c=instrument_ticker, codification=codification).instrument
        try:
            investment = Investment.objects.get(instrument=instrument)
        except ObjectDoesNotExist:
            investment = Investment(instrument=instrument)
            investment.save()
        return instrument, investment
    except ObjectDoesNotExist:
        try:
            marketdatatype = Marketdatatype.objects.get(name_c='Cash')
            instrument = Instrument(
                                    name_c = instrument_ticker,
                                    marketdatatype = marketdatatype,
                                    currency = currency,
                                    main_instrument_b = True,
                                    )
            instrument.save()
            Instrumentsynonym(
                              instrument = instrument,
                              codification = codification,
                              validity_d = datetime.now().date(),
                              code_c = instrument_ticker,
                              ).save()
                              
            investment = Investment(instrument=instrument)
            investment.save()
            
            return instrument, investment
        except Exception as e:
            pass
        
        
    

def new_instrument(instrument_ticker, ticker_type, market_data_type, currency=None, underlying_curreny=None, market=None, country=None, risk_country=None, active=True):
    '''
    
    @param instrument_ticker: ticker of the instrument that needs to be inserted
    @param ticker_type: type of ticker (BBG, DS, ISIN)
    @param market_data_type: type of the instrument (Future, German Stock, Index, ...etc)
    @param currency: (Optional) currency in Alpha-3 format
    @param underlying_curreny: (Optional) underlying currency in Alpha-3 format
    @param market: (Optional) if different than the main market that comes from source
    @param active: (Optional) if the synonyms for this instrument are active or not. 
    
    @return: created or found if already existing instrument, and the investment that corresponds to this instrument
    '''
    bbg_errorMsg = []
    ds_errorMsg = []
    
    email_subject = '[QuantServer] Error inserting new instruments'
    
    instrument_metaData_BBG = None
    instrument_metaData_DS = None
    
    market_data_type = Marketdatatype.objects.get(name_c=market_data_type)
    if market == None:
        main_instrument = True
    else:
        main_instrument = False
    try:
        if currency != None:
            currency = Currency.objects.get(isocode_c=currency)
    except ObjectDoesNotExist:
        currency = Currency(
                          isocode_c = currency,
                          name_c = pycountry.currencies.get(alpha_3=currency).name,
                          denomination_c = pycountry.currencies.get(alpha_3=currency).official_name
                          )
        currency.save()
    try:
        if underlying_curreny != None:
            underlying_curreny = Currency.objects.get(isocode_c=underlying_curreny)
    except ObjectDoesNotExist:
        underlying_curreny = Currency(
                          isocode_c = underlying_curreny,
                          name_c = pycountry.currencies.get(alpha_3=underlying_curreny).name,
                          denomination_c = pycountry.currencies.get(alpha_3=underlying_curreny).official_name
                          )
        underlying_curreny.save()
    if market_data_type.type_c == 'Derivative':
        if ticker_type == 'BBG':
            # check if this bloomberg code already exists
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                instrument = Instrumentsynonym.objects.get(code_c=instrument_ticker).instrument
                return instrument, Investment.objects.get(instrument=instrument)
            except ObjectDoesNotExist as e:
                try:
                    instrument_metaData_BBG = get_metaData(instrument_ticker, 'BBG', market_data_type.type_c)
                    try:
                        instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
                    except Exception as e:
                        ds_errorMsg.append('[DS Error]' + instrument_ticker + ':' + str(e))
                except Exception as e:
                    bbg_errorMsg.append('[BBG Error]' + instrument_ticker + ':' + str(e))
        elif ticker_type in ['DS','ISIN']:
            try:
                instrument_metaData_DS = get_metaData(instrument_ticker, 'DS')
                try:
                    instrument_metaData_BBG = get_metaData_ISIN(instrument_metaData_DS['ISIN'], market_data_type.type_c, market)
                    # check if there is an instrument with the same BBG_ticker and market data type
                    try:
                        # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                        inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                        if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                            return inst_syn.instrument, Investment.objects.get(instrument=inst_syn.instrument)
                    except ObjectDoesNotExist as e:
                        pass
                except Exception as e:
                    bbg_errorMsg.append('[BBG Error]' + instrument_ticker + ':' + str(e))
            except Exception as e:
                ds_errorMsg.append('[DS Error]' + instrument_ticker + ':' + str(e))
    else:
        if ticker_type   == 'ISIN':
            try:
                instrument_metaData_BBG = get_metaData_ISIN(instrument_ticker, market_data_type.type_c, market)
                # check if there is an instrument with the same BBG_ticker and market data type
                try:
                    # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                    inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                    if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                        return inst_syn.instrument, Investment.objects.get(instrument=inst_syn.instrument)
                except ObjectDoesNotExist as e:
                    pass
            except Exception as e:
                bbg_errorMsg.append('[BBG Error]' + instrument_ticker + ':' + str(e))
            
            try:
                instrument_metaData_DS = get_metaData(instrument_ticker, 'DS')
                if not instrument_metaData_BBG:
                    inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_DS['DS_Ticker'])
                    if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c and inst_syn.instrument.market == market:
                        ds_errorMsg.append('[DS Error] no new instrument is inserted because there is already one with the same datastream ticker')
                        email_msg = '\n'.join(bbg_errorMsg) + '\n' + '\n'.join(ds_errorMsg) + '\n' + str(instrument_ticker + ':' + e)             
                        send_email('MShama@quantcapital.de;GJi@quantcapital.de', email_subject, email_msg)
                        return inst_syn.instrument, Investment.objects.get(instrument=inst_syn.instrument)
            except Exception as e:
                ds_errorMsg.append('[DS Error]' + instrument_ticker + ':' + str(e))
                
        elif ticker_type == 'BBG':
            # check if this bloomberg code already exists
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                return Instrumentsynonym.objects.get(code_c=instrument_ticker).instrument
            except ObjectDoesNotExist as e:
                try:
                    instrument_metaData_BBG = get_metaData(instrument_ticker, 'BBG', market_data_type.type_c)
                    try:
                        instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
                    except Exception as e:
                        ds_errorMsg.append('[DS Error]' + instrument_ticker + ':' + str(e))
                except Exception as e:
                    bbg_errorMsg.append('[BBG Error]' + instrument_ticker + ':' + str(e))                
        elif ticker_type == 'DS':
            try:     
                instrument_metaData_DS = get_metaData(instrument_ticker, 'DS')
                try:
                    instrument_metaData_BBG = get_metaData_ISIN(instrument_metaData_DS['ISIN'], market_data_type.type_c, market)
                    # check if there is an instrument with the same BBG_ticker and market data type
                    try:
                        # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                        inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                        if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                            return inst_syn.instrument, Investment.objects.get(instrument=inst_syn.instrument)
                    except ObjectDoesNotExist as e:
                        pass
                except Exception as e:
                    bbg_errorMsg.append('[BBG Error]' + instrument_ticker + ':' + str(e))
                    
                    inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_DS['DS_Ticker'])
                    if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c and inst_syn.instrument.market == market:
                        ds_errorMsg.append('[DS Error] no new instrument is inserted because there is already one with the same datastream ticker')
                        email_msg = '\n'.join(bbg_errorMsg) + '\n' + '\n'.join(ds_errorMsg) + '\n' + str(instrument_ticker + ':' + e)             
                        send_email('MShama@quantcapital.de;GJi@quantcapital.de', email_subject, email_msg)
                        return inst_syn.instrument, Investment.objects.get(instrument=inst_syn.instrument)
            except Exception as e:
                ds_errorMsg.append('[DS Error]' + instrument_ticker + ':' + str(e))
    try:
        # try to select market data based on the value from BBG meta data
        if instrument_metaData_BBG and instrument_metaData_BBG['market'] != None and not market:
            market = Market.objects.get(
                            iso_code_c= instrument_metaData_BBG['market'] if market == None else market
                            )
    except ObjectDoesNotExist:
        # if the market doesn't exist then create it
        market = Market(
                        iso_code_c = instrument_metaData_BBG['market'] if market == None else market,
                        name_c = instrument_metaData_BBG['market'] if market == None else market,
                    )
        market.save()
    try:
        if not country and instrument_metaData_BBG and instrument_metaData_BBG['country'] != None:
            country = Country.objects.get(isocode_c=instrument_metaData_BBG['country'])
        else:
            country = None
    except ObjectDoesNotExist:
        country = Country(
                          isocode_c = instrument_metaData_BBG['country'],
                          name_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['country']).name,
                          denomination_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['country']).official_name
                          )
        country.save()
    
    try:
        if not risk_country and instrument_metaData_BBG and instrument_metaData_BBG['cntry_of_risk'] != None:
            risk_country = Country.objects.get(isocode_c=instrument_metaData_BBG['cntry_of_risk'])
    except ObjectDoesNotExist:
        risk_country = Country(
                          isocode_c = instrument_metaData_BBG['cntry_of_risk'],
                          name_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['cntry_of_risk']).name,
                          denomination_c = pycountry.countries.get(alpha_3=instrument_metaData_BBG['cntry_of_risk']).official_name
                          )
        risk_country.save()
        
    if len(ds_errorMsg) == 0 or len(bbg_errorMsg) == 0:
        try:
            # try to create a new instrument
            instrument = Instrument(
                                    name_c = instrument_metaData_BBG['name'] if (instrument_metaData_BBG and instrument_metaData_BBG['name']!=None) else instrument_metaData_DS['name'],
                                    market = market,
                                    marketdatatype = market_data_type,
                                    country = country,
                                    risk_country = risk_country,
                                    currency = currency, 
                                    underlying_currency = underlying_curreny,
                                    bpv_n = instrument_metaData_BBG['BPV'] if (instrument_metaData_BBG and instrument_metaData_BBG['BPV']!=None) else instrument_metaData_DS['BPV'],
                                    main_instrument_b = main_instrument,
                                )
            instrument.save()
            
            # if the instrument is with type bond we need to read extra data for it
            if (instrument.marketdatatype.name_c == 'Bonds'):
                try:
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
                except Exception as e:
                    ds_errorMsg.append('[Bond Error]' + instrument_ticker + ':' + str(e))
            # insert the synonyms for the current instrument
            if instrument_metaData_DS and instrument_metaData_DS['DS_Ticker'] and instrument_metaData_DS['DS_Ticker'] != 'NA':
                Instrumentsynonym(
                    instrument = instrument,
                    codification = Codification.objects.get(name_c='DS_Ticker'),
                    code_c = instrument_metaData_DS['DS_Ticker'],
                    validity_d = datetime.now().date() if active else None,
                ).save()
            if instrument_metaData_DS and instrument_metaData_DS['DS_Code'] and instrument_metaData_DS['DS_Code'] != 'NA':
                Instrumentsynonym(
                    instrument = instrument,
                    codification = Codification.objects.get(name_c='DS_Code'),
                    code_c = instrument_metaData_DS['DS_Code'],
                    validity_d = datetime.now().date() if active else None,
                ).save()
            if instrument_metaData_BBG and instrument_metaData_BBG['BBG_Ticker'] != None:
                Instrumentsynonym(
                    instrument = instrument,
                    codification = Codification.objects.get(name_c='BBG_Ticker'),
                    code_c = instrument_metaData_BBG['BBG_Ticker'],
                    validity_d = datetime.now().date() if active else None,
                ).save()
            if instrument_metaData_BBG and instrument_metaData_BBG['ISIN'] != None:
                Instrumentsynonym(
                    instrument = instrument,
                    codification = Codification.objects.filter(name_c='ISIN')[0],
                    code_c = instrument_metaData_BBG['ISIN'],
                    validity_d = datetime.now().date() if active else None,
                ).save()
                
            email_msg = '\n'.join(bbg_errorMsg) + '\n' + '\n'.join(ds_errorMsg)
            
            if len(email_msg) > 1:
                send_email('MShama@quantcapital.de;GJi@quantcapital.de', email_subject, email_msg)
                
            # insert a new Investment
            if market_data_type.type_c not in ['Index', 'InterestRate', 'Currency']: 
                investment = Investment(instrument=instrument)
                investment.save()
            else:
                investment = None
            
            
                
            return instrument, investment
        except Exception as e:
            ## we need to collect instruments with errors and send an email containing the errors faced
            ## during the insertion
            
            email_msg = '\n'.join(bbg_errorMsg) + '\n' + '\n'.join(ds_errorMsg) + '\n' + str(instrument_ticker + ':' + e) 
            
            send_email('MShama@quantcapital.de;GJi@quantcapital.de', email_subject, email_msg)
            
            print('Error happened while inserting instrument')
            return None, None
    else:
        email_msg = '\n'.join(bbg_errorMsg) + '\n' + '\n'.join(ds_errorMsg)
        send_email('MShama@quantcapital.de;GJi@quantcapital.de', email_subject, email_msg)
        return None, None
        