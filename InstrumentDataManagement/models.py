from django.db import models

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
        
class Instrument(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=100)  # Field name made lowercase.
    market = models.ForeignKey(Market, models.DO_NOTHING, db_column='Market_ID')  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID', related_name='currency')  # Field name made lowercase.
    marketdatatype = models.ForeignKey(Marketdatatype, models.DO_NOTHING, db_column='MarketDataType_ID')  # Field name made lowercase.
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='Country_ID')
    multiplier_n = models.DecimalField(db_column='Multiplier_N', max_digits=10, decimal_places=3)
    nominal_n = models.DecimalField(db_column='Nominal_N', max_digits=10, decimal_places=3)
    expiry_d = models.DateField(db_column='Expiry_d')
    underlying_currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Underlying_Currency_ID', related_name='underlying_currency')
    contract_forward_rate_n = models.DecimalField(db_column='Contract_Forward_Rate_N', max_digits=10, decimal_places=3)
    maturity_n = models.DecimalField(db_column='Maturity_N', max_digits=10, decimal_places=3)
    bpv_n = models.DecimalField(db_column='BPV_N', max_digits=7, decimal_places=3)
    strike_n = models.DecimalField(db_column='Strike_N', max_digits=10, decimal_places=3)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Instrument'
        
