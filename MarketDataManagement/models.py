from django.db import models
from django.db import transaction

from InstrumentDataManagement.models import Instrument, Market, Marketdatatype, Codification, Country, Currency

# common functions
def createPriceUpdateStatment(obj, update_fields):
    sql = "UPDATE [" + obj._meta.db_table + "] SET "
    for field in update_fields:
        if isinstance(obj._meta.get_field(field), models.ForeignKey):
            sql = sql + obj._meta.get_field(field).column + "=" + str(getattr(obj, obj._meta.get_field(field).attname)) + ","
        else:
            sql = sql + obj._meta.get_field(field).column + "='" + str(getattr(obj, field)) + "',"
    sql = sql[:-1] + " WHERE date_d = '" + str(getattr(obj, 'date')) + "'"
    sql = sql + "AND Instrument_ID = " + str(getattr(obj, 'instrument').id)
    return sql

# Create your models here. 
class DatabaseTable(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    denomincation_c = models.CharField(db_column='Denomination_C', max_length=50)
    datasource_c = models.CharField(db_column='DataSource_C', max_length=10)
    
    def __str__(self):
        return self.denomincation_c;
    
    class Meta:
        managed = False
        db_table = 'DatabaseTable'
        
class GoldenRecordField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    fieldtype_c = models.CharField(db_column='FieldType_C', max_length=50)
    fieldparameters_c = models.CharField(db_column='FieldParameters_C', max_length=50)
    databasetables = models.ManyToManyField(DatabaseTable, through='DatabaseTable_GoldenRecordField_Mapping')
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'GoldenRecordField'
        
class DatasourceField(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    data_source_c = models.CharField(db_column='data_source_c', max_length=10)
    fieldtype_c = models.CharField(db_column='FieldType_C', max_length=50)
    fieldparameters_c = models.CharField(db_column='FieldParameters_C', max_length=50)
    databasetables = models.ManyToManyField(DatabaseTable, through='DatabaseTable_DataSourceField_Mapping')
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'DatasourceField'
    
class DatabaseTable_DataSourceField_Mapping(models.Model):
    databasetable = models.ForeignKey(DatabaseTable, db_column='DatabaseTable_ID')
    datasourcefield = models.ForeignKey(DatasourceField, db_column='DataSourceField_ID')
    
    class Meta:
        managed = False
        db_table = 'DatabaseTable_Field_Mapping'

class DatabaseTable_GoldenRecordField_Mapping(models.Model):
    databasetable = models.ForeignKey(DatabaseTable, db_column='DatabaseTable_ID')
    goldenrecordfield = models.ForeignKey(GoldenRecordField, db_column='GoldenRecordField_ID')
    
    class Meta:
        managed = False
        db_table = 'DatabaseTable_Field_Mapping'
        
        
class MarketDataField_Mapping(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    goldenrecord_field = models.ForeignKey(GoldenRecordField, models.DO_NOTHING, db_column='goldenrecord_field_id')
    datasource_field = models.ForeignKey(DatasourceField, models.DO_NOTHING, db_column='datasource_field_id')
    marketdatatype = models.ForeignKey(Marketdatatype, models.DO_NOTHING, db_column='marketdatatype_id')
    valid_from_d = models.DateField(db_column='valid_from_d')
    valid_to_d = models.DateField(db_column='valid_to_d', blank=True, null=True)
    
    def __str__(self):
        return "[" + self.goldenrecord_field.name_c + "],[" + self.datasource_field.name_c + "]"
    
    class Meta:
        managed = False
        db_table = 'MarketDataField_Mapping'
        unique_together = (('goldenrecord_field', 'datasource_field','marketdatatype', 'valid_from_d', 'valid_to_d'),)

# Datastream tables
class MarketData_Equity_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    p = models.DecimalField(db_column='P', max_digits=12, decimal_places=6)
    p_ib = models.DecimalField(db_column='[P.IB]', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    dm = models.DecimalField(db_column='DM', max_digits=12, decimal_places=6)
    ir = models.DecimalField(db_column='IR', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_DataStream_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Fixed_Income_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    cmpm = models.DecimalField(db_column='CMPM', max_digits=12, decimal_places=6)
    gp = models.DecimalField(db_column='GP', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Derivative_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    ps = models.DecimalField(db_column='PS', max_digits=12, decimal_places=6)
    mp = models.DecimalField(db_column='MP', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    pi = models.DecimalField(db_column='PI', max_digits=12, decimal_places=6)
    ri = models.DecimalField(db_column='RI', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_DataStream_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Currency_DataStream_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID', null=True)
    date = models.DateField(db_column='Date_D', null=True)

    class Meta:
        db_table = 'MarketData_Currency_DataStream_C'
        unique_together = (('instrument', 'date'),)


        
# Bloomberg tables
class MarketData_Equity_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6)
    dur_adj_mid = models.DecimalField(db_column='DUR_ADJ_MID', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Fixed_Income_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    key_rate_dur_6mo = models.DecimalField(db_column='Key_Rate_Dur_6MO', max_digits=12, decimal_places=6)
    key_rate_dur_1yr = models.DecimalField(db_column='Key_Rate_Dur_1YR', max_digits=12, decimal_places=6)
    key_rate_dur_2yr = models.DecimalField(db_column='Key_Rate_Dur_2YR', max_digits=12, decimal_places=6)
    key_rate_dur_3yr = models.DecimalField(db_column='Key_Rate_Dur_3YR', max_digits=12, decimal_places=6)
    key_rate_dur_4yr = models.DecimalField(db_column='Key_Rate_Dur_4YR', max_digits=12, decimal_places=6)
    key_rate_dur_5yr = models.DecimalField(db_column='Key_Rate_Dur_5YR', max_digits=12, decimal_places=6)
    key_rate_dur_6yr = models.DecimalField(db_column='Key_Rate_Dur_6YR', max_digits=12, decimal_places=6)
    key_rate_dur_7yr = models.DecimalField(db_column='Key_Rate_Dur_7YR', max_digits=12, decimal_places=6)
    key_rate_dur_8yr = models.DecimalField(db_column='Key_Rate_Dur_8YR', max_digits=12, decimal_places=6)
    key_rate_dur_9yr = models.DecimalField(db_column='Key_Rate_Dur_9YR', max_digits=12, decimal_places=6)
    key_rate_dur_10yr = models.DecimalField(db_column='Key_Rate_Dur_10YR', max_digits=12, decimal_places=6)
    key_rate_dur_15yr = models.DecimalField(db_column='Key_Rate_Dur_15YR', max_digits=12, decimal_places=6)
    key_rate_dur_20yr = models.DecimalField(db_column='Key_Rate_Dur_20YR', max_digits=12, decimal_places=6)
    key_rate_dur_25yr = models.DecimalField(db_column='Key_Rate_Dur_25YR', max_digits=12, decimal_places=6)
    key_rate_dur_30yr = models.DecimalField(db_column='Key_Rate_Dur_30YR', max_digits=12, decimal_places=6)
    dur_adj_oas_mid = models.DecimalField(db_column='DUR_ADJ_OAS_MID', max_digits=12, decimal_places=6)
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6)
    px_dirty_bid = models.DecimalField(db_column='PX_DIRTY_BID', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Derivative_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6)
    fut_cur_gen_ticker = models.CharField(db_column='FUT_CUR_GEN_TICKER', max_length=50)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Currency_Bloomberg_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID', null=True)
    date = models.DateField(db_column='Date_D', null=True)
    px_last = models.DecimalField(db_column='PX_LAST', max_digits=12, decimal_places=6, null=True)

    class Meta:
        db_table = 'MarketData_Currency_Bloomberg_C'
        unique_together = (('instrument', 'date'),)
        
        
# Golden Record tables
class MarketData_Equity_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    time_t = models.TimeField(db_column='time_t')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

        
class MarketData_Derivative_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    current_contract_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='current_contract_instrument_id', related_name='current_contract_instr')
    following_contract_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='following_contract_instrument_id', related_name='following_contract_instr')
    time_t = models.TimeField(db_column='time_t')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_C'
        unique_together = (('instrument', 'date'),)
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Fixed_Income_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    eod_price_dirty_n = models.DecimalField(db_column='EOD_Price_Dirty_n', max_digits=12, decimal_places=6)
    key_rate_dur_6mo_n = models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', max_digits=12, decimal_places=6)
    key_rate_dur_1yr_n = models.DecimalField(db_column='Key_Rate_Dur_1YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_2yr_n = models.DecimalField(db_column='Key_Rate_Dur_2YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_3yr_n = models.DecimalField(db_column='Key_Rate_Dur_3YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_4yr_n = models.DecimalField(db_column='Key_Rate_Dur_4YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_5yr_n = models.DecimalField(db_column='Key_Rate_Dur_5YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_6yr_n = models.DecimalField(db_column='Key_Rate_Dur_6YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_7yr_n = models.DecimalField(db_column='Key_Rate_Dur_7YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_8yr_n = models.DecimalField(db_column='Key_Rate_Dur_8YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_9yr_n = models.DecimalField(db_column='Key_Rate_Dur_9YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_10yr_n = models.DecimalField(db_column='Key_Rate_Dur_10YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_15yr_n = models.DecimalField(db_column='Key_Rate_Dur_15YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_20yr_n = models.DecimalField(db_column='Key_Rate_Dur_20YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_25yr_n = models.DecimalField(db_column='Key_Rate_Dur_25YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_30yr_n = models.DecimalField(db_column='Key_Rate_Dur_30YR_n', max_digits=12, decimal_places=6)
    effective_duration_n = models.DecimalField(db_column='Effective_Duration_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
        
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_C'
        unique_together = (('instrument', 'date'),)
    
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_InterestRate_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    modified_duration_n = models.DecimalField(db_column='Modified_Duration_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_C'
        unique_together = (('instrument', 'date'),)
    
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()

class MarketData_Index_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d')
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_C'
        unique_together = (('instrument', 'date'),)
    
        
    @transaction.atomic
    def update(self,update_fields):
        from django.db import connection
        cursor = connection.cursor()
        sql = createPriceUpdateStatment(self,update_fields)
        cursor.execute(sql)
        cursor.close()
        
class MarketData_Currency_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID', null=True)
    date = models.DateField(db_column='Date_D', null=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6, null=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6, null=True)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N', null=True)
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N', null=True)

    class Meta:
        db_table = 'MarketData_Currency_C'
        unique_together = (('instrument', 'date'),)

#-------------------------------------------------------------------
# the views for market data to select both current and historical data
#-------------------------------------------------------------------

class MarketData_Equity_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', blank=True, null=True)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Equity_VW'
        unique_together = (('instrument', 'date'),)

        
class MarketData_Derivative_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    current_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='[current_contract_instrument_id]', related_name='current_contract_instr_vw')
    following_contract_instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='[following_contract_instrument_id]', related_name='following_contract_instr_vw')
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Derivative_VW'
        unique_together = (('instrument', 'date'),)

class MarketData_Fixed_Income_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    eod_price_dirty_n = models.DecimalField(db_column='EOD_Price_Dirty_n', max_digits=12, decimal_places=6)
    key_rate_dur_6mo_n = models.DecimalField(db_column='Key_Rate_Dur_6Mo_n', max_digits=12, decimal_places=6)
    key_rate_dur_1yr_n = models.DecimalField(db_column='Key_Rate_Dur_1YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_2yr_n = models.DecimalField(db_column='Key_Rate_Dur_2YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_3yr_n = models.DecimalField(db_column='Key_Rate_Dur_3YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_4yr_n = models.DecimalField(db_column='Key_Rate_Dur_4YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_5yr_n = models.DecimalField(db_column='Key_Rate_Dur_5YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_6yr_n = models.DecimalField(db_column='Key_Rate_Dur_6YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_7yr_n = models.DecimalField(db_column='Key_Rate_Dur_7YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_8yr_n = models.DecimalField(db_column='Key_Rate_Dur_8YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_9yr_n = models.DecimalField(db_column='Key_Rate_Dur_9YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_10yr_n = models.DecimalField(db_column='Key_Rate_Dur_10YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_15yr_n = models.DecimalField(db_column='Key_Rate_Dur_15YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_20yr_n = models.DecimalField(db_column='Key_Rate_Dur_20YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_25yr_n = models.DecimalField(db_column='Key_Rate_Dur_25YR_n', max_digits=12, decimal_places=6)
    key_rate_dur_30yr_n = models.DecimalField(db_column='Key_Rate_Dur_30YR_n', max_digits=12, decimal_places=6)
    effective_duration_n = models.DecimalField(db_column='Effective_Duration_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
        
    class Meta:
        managed = False
        db_table = 'MarketData_Fixed_Income_VW'
        unique_together = (('instrument', 'date'),)
        
class MarketData_InterestRate_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    modified_duration_n = models.DecimalField(db_column='Modified_Duration_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_InterestRate_VW'
        unique_together = (('instrument', 'date'),)

class MarketData_Index_VW(models.Model):
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID')  # Field name made lowercase.
    date = models.DateField(db_column='date_d', primary_key=True)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    time_t = models.TimeField(db_column='time_t', auto_now=True)
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')
    
    class Meta:
        managed = False
        db_table = 'MarketData_Index_VW'
        unique_together = (('instrument', 'date'),)
        
class MarketData_Currency_VW(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')
    date = models.DateField(db_column='Date_D')
    intraday_price_n = models.DecimalField(db_column='Intraday_Price_n', max_digits=12, decimal_places=6)
    eod_price_n = models.DecimalField(db_column='EOD_Price_n', max_digits=12, decimal_places=6)
    eod_log_return_n = models.FloatField(db_column='EOD_Log_Return_N')
    intra_log_return_n = models.FloatField(db_column='Intra_Log_Return_N')

    class Meta:
        managed = False
        db_table = 'MarketData_Currency_VW'
        unique_together = (('instrument', 'date'),)