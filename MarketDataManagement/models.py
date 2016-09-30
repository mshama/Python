from django.db import models
from django.db import transaction

from InstrumentDataManagement.models import Instrument, Market, Marketdatatype, Codification, Country, Currency

# Create your models here. 
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
    valid_from_d = models.DateField(db_column='valid_from_d')
    valid_to_d = models.DateField(db_column='valid_to_d', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'MarketDataField_Mapping'
        unique_together = (('goldenrecord_field', 'datasource_field','marketdatatype', 'valid_from_d', 'valid_to_d'),)

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
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = "UPDATE [" + self._meta.db_table + "] SET "
        for field in update_fields:
            sql = sql + self._meta.get_field(field).column + '=' + str(getattr(self, field)) + ','
        sql = sql[:-1] + " WHERE date_d = '" + str(getattr(self, 'date')) + "'"
        sql = sql + "AND Instrument_ID = " + str(getattr(self, 'instrument').id)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    d = models.DecimalField(db_column='D', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_DataStream_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = "UPDATE [" + self._meta.db_table + "] SET "
        for field in update_fields:
            sql = sql + self._meta.get_field(field).column + '=' + str(getattr(self, field)) + ','
        sql = sql[:-1] + " WHERE date_d = '" + str(getattr(self, 'date')) + "'"
        sql = sql + "AND Instrument_ID = " + str(getattr(self, 'instrument').id)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Bond_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Bond_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = "UPDATE [" + self._meta.db_table + "] SET "
        for field in update_fields:
            sql = sql + self._meta.get_field(field).column + '=' + str(getattr(self, field)) + ','
        sql = sql[:-1] + " WHERE date_d = '" + str(getattr(self, 'date')) + "'"
        sql = sql + "AND Instrument_ID = " + str(getattr(self, 'instrument').id)
        cursor.execute(sql)
        cursor.close()

class MarketData_Derivative_DataStream_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    ps = models.DecimalField(db_column='PS', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = "UPDATE [" + self._meta.db_table + "] SET "
        for field in update_fields:
            sql = sql + self._meta.get_field(field).column + '=' + str(getattr(self, field)) + ','
        sql = sql[:-1] + " WHERE date_d = '" + str(getattr(self, 'date')) + "'"
        sql = sql + "AND Instrument_ID = " + str(getattr(self, 'instrument').id)
        cursor.execute(sql)
        cursor.close()

class MasterData_Stock_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    strike_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Stock_C'
        unique_together = (('instrument', 'date'),)

        
class MarketData_Derivative_C(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    price_n = models.DecimalField(db_column='price_n', max_digits=12, decimal_places=6)
    current_contract_instr = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='current_contract_instr_id', related_name='current_contract_instr')
    following_contract_instr = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='following_contract_instr_id', related_name='following_contract_instr')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_C'
        unique_together = (('instrument', 'date'),)
        
