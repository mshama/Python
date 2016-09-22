from django.db import models


from InstrumentDataManagement.models import Instrument

# Create your models here.
class Marketdatatype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50) # Field name made lowercase.
    type_c = models.CharField(db_column='Type_C', max_length=50)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'MarketDataType'
        
        
class Market(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    iso_code_c = models.CharField(db_column='ISO_Code_C', max_length=3)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50, blank=True, null=True)  # Field name made lowercase.

    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Market'
    
class Currency(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    isocode_c = models.CharField(db_column='ISOCode_C', max_length=3)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Currency'

class Country(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    isocode_c = models.CharField(db_column='ISOCode_C', max_length=3)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Country'
        
class Codification(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Codification'        
                
class GoldenRecordField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'GoldenRecordField'
        
class DatasourceField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    data_source_c = models.CharField(db_column='data_source_c', max_length=10)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'DatasourceField'
        
class MarketDataField_Mapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goldenrecord_field = models.ForeignKey(GoldenRecordField, models.DO_NOTHING, db_column='goldenrecord_field_id')
    datasource_field = models.ForeignKey(DatasourceField, models.DO_NOTHING, db_column='datasource_field_id')
    marketdatatype = models.ForeignKey(Marketdatatype, models.DO_NOTHING, db_column='marketdatatype_id')
    valid_from = models.DateField(db_column='valid_from_d')
    valid_to = models.DateField(db_column='valid_to_d', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'MarketDataField_Mapping'
        unique_together = (('goldenrecord_field', 'datasource_field','marketdatatype', 'valid_from', 'valid_to'),)
        
class MasterData_Stock_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    strike_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    risk_country = models.ForeignKey(Country, models.DO_NOTHING, db_column='risk_country_id')
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='currency_id')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Stock_C'
        unique_together = (('instrument', 'date'),)

class MarketData_Stock_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    p = models.DecimalField(db_column='P', max_digits=12, decimal_places=6)
    pi = models.DecimalField(db_column='PI', max_digits=12, decimal_places=6)
    p_ib = models.DecimalField(db_column='[P.IB]', max_digits=12, decimal_places=6)
    ri = models.DecimalField(db_column='RI', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Stock_DataStream_C'
        unique_together = (('instrument', 'date'),)
        
class MarketData_Derivative_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    price_n = models.DecimalField(db_column='price_n', max_digits=12, decimal_places=6)
    current_contract_instr = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='current_contract_instr_id', related_name='current_contract_instr')
    following_contract_instr = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='following_contract_instr_id', related_name='following_contract_instr')
    risk_country = models.ForeignKey(Country, models.DO_NOTHING, db_column='risk_country_id')
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='currency_id')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_C'
        unique_together = (('instrument', 'date'),)
        
