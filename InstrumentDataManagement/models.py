from django.db import models

from django.db import transaction


# Create your models here.
class Marketdatatype(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50) # Field name made lowercase.
    type_c = models.CharField(db_column='Type_C', max_length=50)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        #managed = False
        db_table = 'MarketDataType'
        unique_together = (('name_c',))
        
        
        
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
        return self.isocode_c
    
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
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50, blank=True, null=True)  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Codification'
        
class Instrument(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=100, blank=True, null=True)  # Field name made lowercase.
    market = models.ForeignKey(Market, models.DO_NOTHING, db_column='Market_ID', blank=True, null=True)  # Field name made lowercase.
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID', related_name='currency', blank=True, null=True)  # Field name made lowercase.
    marketdatatype = models.ForeignKey(Marketdatatype, models.DO_NOTHING, db_column='MarketDataType_ID')  # Field name made lowercase.
    country = models.ForeignKey(Country, models.DO_NOTHING, db_column='Country_ID', related_name='country', blank=True, null=True)
    risk_country = models.ForeignKey(Country, models.DO_NOTHING, db_column='risk_country_id', related_name='risk_country', blank=True, null=True)
    multiplier_n = models.DecimalField(db_column='Multiplier_N', max_digits=10, decimal_places=3, blank=True, null=True)
    expiry_d = models.DateField(db_column='Expiry_d', blank=True, null=True)
    underlying_currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Underlying_Currency_ID', related_name='underlying_currency', blank=True, null=True)
    contract_forward_rate_n = models.DecimalField(db_column='Contract_Forward_Rate_N', max_digits=10, decimal_places=3, blank=True, null=True)
    maturity_n = models.DecimalField(db_column='Maturity_N', max_digits=10, decimal_places=3, blank=True, null=True)
    bpv_n = models.DecimalField(db_column='BPV_N', max_digits=12, decimal_places=3, blank=True, null=True)
    strike_n = models.DecimalField(db_column='Strike_N', max_digits=10, decimal_places=3, blank=True, null=True)
    main_instrument_b = models.BooleanField(db_column='Main_Instrument_B', blank=True)
    
    def __str__(self):
        return self.name_c
    
    def complete_name(self):
        instrumentsyn = Instrumentsynonym.objects.filter(instrument=self)
        code_c = self.name_c
        for syno in instrumentsyn:
            code_c = code_c + '\\[' + syno.codification.name_c + ']' + syno.code_c
        return code_c
    
    class Meta:
        managed = False
        db_table = 'Instrument'
        

class Bond(models.Model):
    instrument = models.OneToOneField(Instrument, on_delete=models.CASCADE, db_column='instrument_id', primary_key=True)
    nominal_n = models.DecimalField(db_column='nominal_n', max_digits=12, decimal_places=6, blank=True, null=True)
    life_n = models.DecimalField(db_column='life_n', max_digits=12, decimal_places=6, blank=True, null=True)
    coupon_current_n = models.DecimalField(db_column='coupon_current_n', max_digits=12, decimal_places=6, blank=True, null=True)
    coupon_floating_n = models.DecimalField(db_column='coupon_floating_n', max_digits=12, decimal_places=6, blank=True, null=True)
    floating_real_margin_n = models.DecimalField(db_column='floating_real_margin_n', max_digits=12, decimal_places=6, blank=True, null=True)
    #redemption_n =  models.DecimalField(db_column='redemption_n', max_digits=12, decimal_places=6, blank=True, null=True)
    amortisationtype_c = models.CharField(db_column='amortisationtype_c', max_length=50)
    bondtype_c = models.CharField(db_column='bondtype_c', max_length=50)
    
    def __str__(self):
        return self.instrument.name_c
    
    class Meta:
        managed = False
        db_table = 'Bond'


from PortfolioPositionManagement.models import Mandate

class AssetClass(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    name_c = models.CharField(db_column='Name_C', max_length=50)  # Field name made lowercase.
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50, blank=True, null=True)  # Field name made lowercase.
    parent_assetclass = models.ForeignKey('AssetClass', models.DO_NOTHING, db_column='parent_assetclass_id', null=True)  # Field name made lowercase.
    level_n = models.IntegerField(db_column='Level_N')  # Field name made lowercase.
    
    def __str__(self):
        return self.name_c
        
    class Meta:
        managed = False
        db_table = 'AssetClass'
        
class AssetClass_Instrument(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    assetclass = models.ForeignKey(AssetClass, models.DO_NOTHING, db_column='AssetClass_ID')  # Field name made lowercase.
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    mandate = models.ForeignKey(Mandate, models.DO_NOTHING, db_column='Mandate_ID')
    
    class Meta:
        managed = False
        db_table = 'AssetClass_Instrument'
        unique_together = (('assetclass', 'instrument','mandate'))
        
class Instrumentsynonym(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    codification = models.ForeignKey(Codification, models.DO_NOTHING, db_column='Codification_ID')  # Field name made lowercase.
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE, db_column='Instrument_ID')  # Field name made lowercase.
    validity_d = models.DateField(db_column='Validity_D', blank=True, null=True, default=False)  # Field name made lowercase.
    code_c = models.CharField(db_column='Code_C', max_length=50)  # Field name made lowercase.

    def __str__(self):
        return self.code_c

    class Meta:
        managed = False
        db_table = 'InstrumentSynonym'
        unique_together = (('code_c', 'instrument', 'codification'), ('instrument', 'codification'))
