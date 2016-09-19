'''
Created on 24.08.2016

this file contains all models we need to pick what we want for our apps and add them to model.py in this app

@author: Moustafa Shama
'''
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models

class Alert(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    alerttype_id = models.IntegerField(db_column='AlertType_ID')  # Field name made lowercase.
    scope_c = models.CharField(db_column='Scope_C', max_length=50)  # Field name made lowercase.
    active_f = models.BooleanField(db_column='Active_F')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Alert'


class Alerttype(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AlertType'


class Assetclass(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AssetClass'


class AssetclassInstrument(models.Model):
    assetclass = models.ForeignKey(Assetclass, models.DO_NOTHING, db_column='AssetClass_ID')  # Field name made lowercase.
    instrument = models.ForeignKey('Instrument', models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    level_n = models.DecimalField(db_column='Level_N', max_digits=10, decimal_places=5)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'AssetClass_Instrument'


class Codification(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Codification'


class Currency(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    isocode_c = models.CharField(db_column='ISOCode_C', max_length=3)  # Field name made lowercase.
    denomination = models.CharField(db_column='Denomination', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Currency'


class Derivativedata(models.Model):
    instrument = models.ForeignKey('Instrument', models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'DerivativeData'


class Event(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    alert = models.ForeignKey(Alert, models.DO_NOTHING, db_column='Alert_ID')  # Field name made lowercase.
    description_c = models.CharField(db_column='Description_C', max_length=50)  # Field name made lowercase.
    event_dt = models.DateTimeField(db_column='Event_DT')  # Field name made lowercase.
    confirm_f = models.BooleanField(db_column='Confirm_F')  # Field name made lowercase.
    confirm_user = models.ForeignKey('User', models.DO_NOTHING, db_column='Confirm_user_ID')  # Field name made lowercase.
    confirm_dt = models.DateTimeField(db_column='Confirm_DT')  # Field name made lowercase.
    confirm_comment_c = models.CharField(db_column='Confirm_Comment_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Event'


class ExchangerateC(models.Model):
    reference_currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Reference_Currency_ID')  # Field name made lowercase.
    underlying_currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Underlying_Currency_ID')  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', primary_key=True, max_length=10)  # Field name made lowercase.
    type_c = models.CharField(db_column='Type_C', max_length=50)  # Field name made lowercase.
    price_n = models.DecimalField(db_column='Price_N', max_digits=30, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ExchangeRate_C'


class Function(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Function'


class FunctionProfile(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    function = models.ForeignKey(Function, models.DO_NOTHING, db_column='Function_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Function_Profile'


class FunctionProfileComposition(models.Model):
    function = models.ForeignKey(Function, models.DO_NOTHING, db_column='Function_ID')  # Field name made lowercase.
    function_profile = models.ForeignKey(FunctionProfile, models.DO_NOTHING, db_column='Function_Profile_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Function_Profile_Composition'


class Group(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.
    function_profile = models.ForeignKey(FunctionProfile, models.DO_NOTHING, db_column='Function_Profile_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Group'


class Instrument(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=100)  # Field name made lowercase.
    market = models.ForeignKey('Market', models.DO_NOTHING, db_column='Market_ID')  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID')  # Field name made lowercase.
    marketdatatype = models.ForeignKey('Marketdatatype', models.DO_NOTHING, db_column='MarketDataType_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Instrument'


class Instrumentcompo(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parent_instrument_id = models.IntegerField(db_column='Parent_Instrument_ID')  # Field name made lowercase.
    field_instrument_id = models.IntegerField(db_column='[Instrument:_ID')  # Field name made lowercase. Field renamed to remove unsuitable characters. Field renamed because it started with '_'.
    status_id = models.IntegerField(db_column='Status_ID')  # Field name made lowercase.
    position_date_d = models.CharField(db_column='Position_Date_D', max_length=10)  # Field name made lowercase.
    currency_id = models.IntegerField(db_column='Currency_ID')  # Field name made lowercase.
    quantity_n = models.DecimalField(db_column='Quantity_N', max_digits=30, decimal_places=10)  # Field name made lowercase.
    price_n = models.DecimalField(db_column='Price_N', max_digits=30, decimal_places=2)  # Field name made lowercase.
    exchangerate_n = models.DecimalField(db_column='ExchangeRate_N', max_digits=10, decimal_places=4)  # Field name made lowercase.
    amount_n = models.DecimalField(db_column='Amount_N', max_digits=30, decimal_places=10)  # Field name made lowercase.
    importedposition_b = models.BooleanField(db_column='ImportedPosition_B')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InstrumentCompo'


class Instrumentsynonym(models.Model):
    codification = models.ForeignKey(Codification, models.DO_NOTHING, db_column='Codification_ID')  # Field name made lowercase.
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    validity_d = models.AutoField(db_column='Validity_D', primary_key=True)  # Field name made lowercase.
    code_c = models.CharField(db_column='Code_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'InstrumentSynonym'


class Investment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID', blank=True, null=True)  # Field name made lowercase.
    portfolio = models.ForeignKey('Portfolio', models.DO_NOTHING, db_column='Portfolio_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Investment'
        unique_together = (('portfolio', 'instrument'),)


class Mandate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    portfolio = models.ForeignKey('Portfolio', models.DO_NOTHING, db_column='Portfolio_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Mandate'


class Market(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    iso_code_c = models.CharField(db_column='ISO_Code_C', max_length=3)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination = models.CharField(db_column='Denomination', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Market'


class Marketdatatype(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    type_c = models.CharField(db_column='Type_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'MarketDataType'


class MarketdataBond(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond'
        unique_together = (('instrument', 'date_d'),)


class MarketdataBondBloomberg(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond_Bloomberg'
        unique_together = (('instrument', 'date_d'),)


class MarketdataBondBloombergH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond_Bloomberg_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataBondDatastream(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond_DataStream'
        unique_together = (('instrument', 'date_d'),)


class MarketdataBondDatastreamH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond_DataStream_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataBondH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Bond_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivative(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivativeBloomberg(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_Bloomberg'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivativeBloombergH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_Bloomberg_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivativeDatastream(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_DataStream'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivativeDatastreamH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_DataStream_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataDerivativeH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrate(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrateBloomberg(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_Bloomberg'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrateBloombergH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_Bloomberg_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrateDatastream(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_DataStream'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrateDatastreamH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_DataStream_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataInterestrateH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStock(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStockBloomberg(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock_Bloomberg'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStockBloombergH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock_Bloomberg_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStockDatastream(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock_DataStream'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStockDatastreamH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock_DataStream_H'
        unique_together = (('instrument', 'date_d'),)


class MarketdataStockH(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING)
    date_d = models.CharField(max_length=10)

    class Meta:
        managed = False
        db_table = 'MarketData_Stock_H'
        unique_together = (('instrument', 'date_d'),)


class Parameter(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parameter_c = models.CharField(db_column='Parameter_C', max_length=50)  # Field name made lowercase.
    value_c = models.CharField(db_column='Value_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Parameter'


class Parameterset(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    parameter = models.ForeignKey(Parameter, models.DO_NOTHING, db_column='Parameter_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ParameterSet'


class Portfolio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    activeflag_b = models.BooleanField(db_column='ActiveFlag_B')  # Field name made lowercase.
    create_user = models.ForeignKey('User', models.DO_NOTHING, db_column='Create_User_ID')  # Field name made lowercase.
    create_d = models.CharField(db_column='Create_D', max_length=10)  # Field name made lowercase.
    last_modf_user_id = models.IntegerField(db_column='Last_Modf_User_ID')  # Field name made lowercase.
    last_modf_d = models.CharField(db_column='Last_Modf_D', max_length=10)  # Field name made lowercase.
    primary_riskmodel_id = models.IntegerField(db_column='Primary_Riskmodel_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Portfolio'


class Position(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')  # Field name made lowercase.
    investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Investment_ID')  # Field name made lowercase.
    status = models.ForeignKey('Status', models.DO_NOTHING, db_column='Status_ID')  # Field name made lowercase.
    valuedate_d = models.CharField(db_column='ValueDate_D', max_length=10)  # Field name made lowercase.
    quantity_n = models.DecimalField(db_column='Quantity_N', max_digits=30, decimal_places=10)  # Field name made lowercase.
    amount_n = models.DecimalField(db_column='Amount_N', max_digits=18, decimal_places=2)  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Position'


class Positionvaluationprocess(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', max_length=10)  # Field name made lowercase.
    start_d = models.CharField(db_column='Start_D', max_length=10)  # Field name made lowercase.
    end_d = models.CharField(db_column='End_D', max_length=10)  # Field name made lowercase.
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')  # Field name made lowercase.
    status_c = models.CharField(db_column='Status_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'PositionValuationProcess'


class Processtype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ProcessType'


class Reportingprocess(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    processtype = models.ForeignKey(Processtype, models.DO_NOTHING, db_column='ProcessType_ID')  # Field name made lowercase.
    start_dt = models.DateTimeField(db_column='Start_DT')  # Field name made lowercase.
    end_dt = models.DateTimeField(db_column='End_DT')  # Field name made lowercase.
    parameterset = models.ForeignKey(Parameterset, models.DO_NOTHING, db_column='ParameterSet_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ReportingProcess'


class Resultset(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    reportingprocess = models.ForeignKey(Reportingprocess, models.DO_NOTHING, db_column='ReportingProcess_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ResultSet'


class ResultAllocationreport(models.Model):
    result = models.ForeignKey(Resultset, models.DO_NOTHING, db_column='Result_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Result_AllocationReport'


class ResultAssetreport(models.Model):
    resultset = models.ForeignKey(Resultset, models.DO_NOTHING, db_column='ResultSet_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Result_AssetReport'


class ResultPerformancereport(models.Model):
    resultset = models.ForeignKey(Resultset, models.DO_NOTHING, db_column='ResultSet_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Result_PerformanceReport'


class ResultRiskreport(models.Model):
    resultset = models.ForeignKey(Resultset, models.DO_NOTHING, db_column='ResultSet_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Result_RiskReport'


class Riskclass(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    valuelimit = models.ForeignKey('Valuelimit', models.DO_NOTHING, db_column='ValueLimit_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskclass'


class RiskclassRiskfactor(models.Model):
    riskfactor = models.ForeignKey('Riskfactor', models.DO_NOTHING, db_column='Riskfactor_ID')  # Field name made lowercase.
    riskclass = models.ForeignKey(Riskclass, models.DO_NOTHING, db_column='RiskClass_ID')  # Field name made lowercase.
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskclass_Riskfactor'


class Riskfactor(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    riskfactorinsturment = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='RiskfactorInsturment_ID')  # Field name made lowercase.
    riskfactorcomposition = models.ForeignKey('Riskfactorcomposition', models.DO_NOTHING, db_column='RiskfactorComposition_ID')  # Field name made lowercase.
    hedgeinstrument_id = models.IntegerField(db_column='HedgeInstrument_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskfactor'


class Riskfactorcomposition(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    riskfactor = models.ForeignKey(Riskfactor, models.DO_NOTHING, db_column='Riskfactor_ID')  # Field name made lowercase.
    weight = models.DecimalField(db_column='Weight', max_digits=5, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RiskfactorComposition'


class RiskfactorRefinstrument(models.Model):
    riskfactor_refinstrument_id = models.IntegerField(db_column='Riskfactor_RefInstrument_ID', primary_key=True)  # Field name made lowercase.
    referenceinstrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='ReferenceInstrument_ID')  # Field name made lowercase.
    mandate = models.ForeignKey(Mandate, models.DO_NOTHING, db_column='Mandate_ID')  # Field name made lowercase.
    riskfactor = models.ForeignKey(Riskfactor, models.DO_NOTHING, db_column='Riskfactor_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskfactor_RefInstrument'


class Riskmodel(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    description_c = models.CharField(db_column='Description_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskmodel'


class Riskmodelconfiguration(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    riskmodel = models.ForeignKey(Riskmodel, models.DO_NOTHING, db_column='Riskmodel_ID')  # Field name made lowercase.
    valid_from_d = models.CharField(db_column='Valid_From_D', max_length=10)  # Field name made lowercase.
    valid_to_d = models.CharField(db_column='Valid_To_D', max_length=10)  # Field name made lowercase.
    holding_period_n = models.DecimalField(db_column='Holding_Period_N', max_digits=18, decimal_places=2)  # Field name made lowercase.
    confidence_level_n = models.DecimalField(db_column='Confidence_Level_N', max_digits=6, decimal_places=3)  # Field name made lowercase.
    cornisch_fischer_b = models.BooleanField(db_column='Cornisch_Fischer_B')  # Field name made lowercase.
    volatility_estimation_c = models.CharField(db_column='Volatility_Estimation_C', max_length=10)  # Field name made lowercase.
    persistence_n = models.DecimalField(db_column='Persistence_N', max_digits=6, decimal_places=3)  # Field name made lowercase.
    frequency_n = models.DecimalField(db_column='Frequency_N', max_digits=18, decimal_places=3)  # Field name made lowercase.
    lookbackwindow_n = models.DecimalField(db_column='LookbackWindow_N', max_digits=18, decimal_places=3)  # Field name made lowercase.
    beta_frequency_n = models.DecimalField(db_column='Beta_Frequency_N', max_digits=18, decimal_places=3)  # Field name made lowercase.
    beta_lookbackwindow_n = models.DecimalField(db_column='Beta_LookbackWindow_N', max_digits=18, decimal_places=3)  # Field name made lowercase.
    beta_persistence_n = models.DecimalField(db_column='Beta_Persistence_N', max_digits=18, decimal_places=3)  # Field name made lowercase.
    liquidity_class_n = models.DecimalField(db_column='Liquidity_Class_N', max_digits=18, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'RiskmodelConfiguration'


class Riskrawdata(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    creation_dt = models.DateTimeField(db_column='Creation_DT')  # Field name made lowercase.
    riskfactor_refinstrument_id = models.IntegerField(db_column='Riskfactor_RefInstrument_ID')  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', max_length=10)  # Field name made lowercase.
    logreturnofprice = models.DecimalField(db_column='LogReturnOfPrice', max_digits=30, decimal_places=15)  # Field name made lowercase.
    decay_n = models.DecimalField(db_column='Decay_N', max_digits=30, decimal_places=15)  # Field name made lowercase.
    volatility_n = models.DecimalField(db_column='Volatility_N', max_digits=30, decimal_places=15)  # Field name made lowercase.
    skew_n = models.DecimalField(db_column='Skew_N', max_digits=30, decimal_places=15)  # Field name made lowercase.
    kurtosis_n = models.DecimalField(db_column='Kurtosis_N', max_digits=30, decimal_places=15)  # Field name made lowercase.
    instrument = models.ForeignKey(RiskfactorRefinstrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    beta_n = models.DecimalField(db_column='Beta_N', max_digits=30, decimal_places=15)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskrawdata'


class Signaltrigger(models.Model):
    riskclass = models.ForeignKey(Riskclass, models.DO_NOTHING, db_column='Riskclass_ID')  # Field name made lowercase.
    alpha_min_n = models.DecimalField(db_column='Alpha_Min_N', max_digits=5, decimal_places=4)  # Field name made lowercase.
    alpha_max_n = models.DecimalField(db_column='Alpha_Max_N', max_digits=5, decimal_places=4)  # Field name made lowercase.
    targetexposure_n = models.DecimalField(db_column='TargetExposure_N', max_digits=5, decimal_places=4)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'SignalTrigger'


class Status(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Status'


class Transaction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')  # Field name made lowercase.
    investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Investment_ID')  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID')  # Field name made lowercase.
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='Status_ID')  # Field name made lowercase.
    type = models.ForeignKey('Type', models.DO_NOTHING, db_column='Type_ID')  # Field name made lowercase.
    quantity_n = models.DecimalField(db_column='Quantity_N', max_digits=30, decimal_places=10)  # Field name made lowercase.
    price_n = models.DecimalField(db_column='Price_N', max_digits=18, decimal_places=2)  # Field name made lowercase.
    exchangerate_n = models.DecimalField(db_column='ExchangeRate_N', max_digits=10, decimal_places=4)  # Field name made lowercase.
    amount_n = models.DecimalField(db_column='Amount_N', max_digits=18, decimal_places=2)  # Field name made lowercase.
    tradedate_d = models.CharField(db_column='TradeDate_D', max_length=10)  # Field name made lowercase.
    valuedate_d = models.CharField(db_column='ValueDate_D', max_length=10)  # Field name made lowercase.
    create_user = models.ForeignKey('User', models.DO_NOTHING, db_column='Create_User_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Transaction'


class Type(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Type'


class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User'


class UserGroup(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='User_ID')  # Field name made lowercase.
    group = models.ForeignKey(Group, models.DO_NOTHING, db_column='Group_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'User_Group'


class Valuelimit(models.Model):
    id = models.IntegerField(db_column='ID', primary_key=True)  # Field name made lowercase.
    lower_valuelimit_n = models.DecimalField(db_column='Lower_ValueLimit_N', max_digits=18, decimal_places=0)  # Field name made lowercase.
    valid_from_d = models.CharField(db_column='Valid_From_D', max_length=10)  # Field name made lowercase.
    valid_to_d = models.CharField(db_column='Valid_To_D', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ValueLimit'