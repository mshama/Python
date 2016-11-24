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


sys.path.append(os.path.abspath("../../QuantServer/"))
os.environ['DJANGO_SETTINGS_MODULE'] = 'QuantServer.settings'

django.setup()

from datetime import datetime

from InstrumentDataManagement.models import Instrumentsynonym, Instrument, Marketdatatype,\
    Currency, Market, Country, Bond, Codification
from dataconnections.datasource import get_metaData, get_bond_metaData, get_metaData_ISIN


def new_instrument(instrument_ticker, ticker_type, market_data_type, currency, underlying_curreny, market=None, active=True):
    market_data_type = Marketdatatype.objects.get(name_c=market_data_type)
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
                return Instrumentsynonym.objects.get(code_c=instrument_ticker).instrument                
            except ObjectDoesNotExist as e:
                instrument_metaData_BBG = get_metaData(instrument_ticker, 'BBG', market_data_type.type_c)
                instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
        elif ticker_type in ['DS','ISIN']:
            instrument_metaData_DS = get_metaData(instrument_ticker, 'DS')
            instrument_metaData_BBG = get_metaData_ISIN(instrument_metaData_DS['ISIN'], market_data_type.type_c, market)
            # check if there is an instrument with the same BBG_ticker and market data type
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                    return inst_syn.instrument
            except ObjectDoesNotExist as e:
                pass
    else:
        if ticker_type   == 'ISIN':
            instrument_metaData_BBG = get_metaData_ISIN(instrument_ticker, market_data_type.type_c, market)
            # check if there is an instrument with the same BBG_ticker and market data type
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                    return inst_syn.instrument
            except ObjectDoesNotExist as e:
                instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
        elif ticker_type == 'BBG':
            # check if this bloomberg code already exists
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                return Instrumentsynonym.objects.get(code_c=instrument_ticker).instrument
            except ObjectDoesNotExist as e:
                instrument_metaData_BBG = get_metaData(instrument_ticker, 'BBG', market_data_type.type_c)
                instrument_metaData_DS = get_metaData(instrument_metaData_BBG['ISIN'], 'DS')
        elif ticker_type == 'DS':
            instrument_metaData_DS = get_metaData(instrument_ticker, 'DS')
            instrument_metaData_BBG = get_metaData_ISIN(instrument_metaData_DS['ISIN'], market_data_type.type_c, market)
            # check if there is an instrument with the same BBG_ticker and market data type
            try:
                # if Bloomberg code exists then this instrument already exists we do not need to insert any new instrument or synonym
                inst_syn = Instrumentsynonym.objects.get(code_c=instrument_metaData_BBG['BBG_Ticker'])
                if inst_syn.instrument.marketdatatype.name_c == market_data_type.name_c:
                    return inst_syn.instrument
            except ObjectDoesNotExist as e:
                pass
    try:
        # try to select market data based on the value from BBG meta data
        if instrument_metaData_BBG['market'] != None or market != None:
            market = Market.objects.get(
                            iso_code_c= instrument_metaData_BBG['market'] if market == None else market
                            )
        else:
            market = None
    except ObjectDoesNotExist:
        # if the market doesn't exist then create it
        market = Market(
                        iso_code_c = instrument_metaData_BBG['market'] if market == None else market,
                        name_c = instrument_metaData_BBG['market'] if market == None else market,
                    )
        market.save()
    try:
        if instrument_metaData_BBG['country'] != None:
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
        if instrument_metaData_BBG['cntry_of_risk'] != None:
            risk_country = Country.objects.get(isocode_c=instrument_metaData_BBG['cntry_of_risk'])
        else:
            risk_country = None
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
                                marketdatatype = market_data_type,
                                country = country,
                                risk_country = risk_country,
                                currency = currency, 
                                underlying_currency = underlying_curreny,
                                bpv_n = instrument_metaData_BBG['BPV'],
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
        if instrument_metaData_DS['DS_Ticker'] and instrument_metaData_DS['DS_Ticker'] != 'NA':
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.get(name_c='DS_Ticker'),
                code_c = instrument_metaData_DS['DS_Ticker'],
                validity_d = datetime.now().date() if active else None,
            ).save()
        if instrument_metaData_DS['DS_Code'] and instrument_metaData_DS['DS_Code'] != 'NA':
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.get(name_c='DS_Code'),
                code_c = instrument_metaData_DS['DS_Code'],
                validity_d = datetime.now().date() if active else None,
            ).save()
        if instrument_metaData_BBG['BBG_Ticker'] != None:
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.get(name_c='BBG_Ticker'),
                code_c = instrument_metaData_BBG['BBG_Ticker'],
                validity_d = datetime.now().date() if active else None,
            ).save()
        if instrument_metaData_BBG['ISIN'] != None:
            Instrumentsynonym(
                instrument = instrument,
                codification = Codification.objects.filter(name_c='ISIN')[0],
                code_c = instrument_metaData_BBG['ISIN'],
                validity_d = datetime.now().date() if active else None,
            ).save()
        return instrument
    except Exception as e:
        ## we need to collect instruments with errors and send an email containing the errors faced
        ## during the insertion
        print('Error happened while inserting instrument')
        return None
        