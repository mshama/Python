from django.db import models
from pymc.Container import value_doc

from UserManagement.models import User, Group

# Create your models here.

class Mandate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Mandate'

from RiskModelManagement.models import RiskModel
        
class Portfolio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    activeflag_b = models.BooleanField(db_column='ActiveFlag_B', blank=True)
    create_user = models.ForeignKey(User, models.DO_NOTHING, db_column='Create_User_ID', related_name='portfolio_create_user')
    create_d = models.DateField(db_column='Create_D')
    last_modf_user = models.ForeignKey(User, models.DO_NOTHING, db_column='Last_Modf_User_ID', related_name='last_modf_user', blank=True, null=True)
    last_modf_d = models.DateField(db_column='Last_Modf_D', blank=True, null=True)
    primary_riskmodel = models.ForeignKey(RiskModel, models.DO_NOTHING, db_column='Primary_Riskmodel_ID')
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Portfolio'
        
class Mandate_Portfolio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')
    mandate = models.ForeignKey(Mandate, models.DO_NOTHING, db_column='Mandate_ID')
    
    class Meta:
        managed = False
        db_table = 'Mandate'
    

from InstrumentDataManagement.models import Instrument, Currency
        
class Investment(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID', blank=True, null=True)
    instrument = models.ForeignKey(Instrument, models.DO_NOTHING, db_column='Instrument_ID', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Investment'
        
class Status(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Status'
        
class Type(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Type'


        
class Position(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    parent_investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Parent_Investment_ID', related_name='position_parent_investment', blank=True, null=True)
    investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Investment_ID', related_name='position_investment', blank=True, null=True)
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='Status_ID', blank=True, null=True)
    positiondatefrom_d = models.DateField(db_column='PositionDateFrom_D', blank=True, null=True)
    positiondateto_d = models.DateField(db_column='PositionDateTo_D', blank=True, null=True)
    quantity_n = models.DecimalField(db_column='Quantity_N', max_digits=30, decimal_places=10, blank=True, null=True)
    price_cost_n = models.DecimalField(db_column='Price_Cost_N', max_digits=18, decimal_places=2, blank=True, null=True)
    price_valuation_kvg_n = models.DecimalField(db_column='Price_Valuation_KVG_N', max_digits=18, decimal_places=0, blank=True, null=True)
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID', blank=True, null=True)
    exchangerate_n = models.DecimalField(db_column='ExchangeRate_N', max_digits=10, decimal_places=4, blank=True, null=True)
    original_input_usergroup = models.ForeignKey(Group, models.DO_NOTHING, db_column='Original_Input_UserGroup_ID', related_name='position_original_input_user_group', blank=True, null=True)
    market_value_kvg_eur_n = models.DecimalField(db_column='Market_Value_KVG_EUR_N', max_digits=30, decimal_places=10, blank=True, null=True)
    market_value_kvg_fc_n = models.DecimalField(db_column='Market_Value_KVG_FC_N', max_digits=30, decimal_places=10, blank=True, null=True)
    market_data_type_c = models.CharField(db_column='Market_Data_Type_C', max_length=50)
    nominal_value_bond_n = models.DecimalField(db_column='Nominal_Value_Bond_N', max_digits=18, decimal_places=2, blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Position'
        unique_together = (('parent_investment', 'investment','status', 'positiondatefrom_d', 'original_input_usergroup'),)
        
class Transaction(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    parent_investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Parent_Investment_ID', related_name='transaction_parent_investment')
    investment = models.ForeignKey(Investment, models.DO_NOTHING, db_column='Investment_ID', related_name='transaction_investment')
    currency = models.ForeignKey(Currency, models.DO_NOTHING, db_column='Currency_ID')
    status = models.ForeignKey(Status, models.DO_NOTHING, db_column='Status_ID')
    type = models.ForeignKey(Type, models.DO_NOTHING, db_column='Type_ID')
    quantity_n = models.DecimalField(db_column='Quantity_N', max_digits=30, decimal_places=10, blank=True, null=True)
    price_n = models.DecimalField(db_column='Price_N', max_digits=18, decimal_places=2)
    exchangerate_n = models.DecimalField(db_column='ExchangeRate_N', max_digits=10, decimal_places=4)
    volumne_eur_n = models.DecimalField(db_column='Volume_EUR_N', max_digits=18, decimal_places=2, blank=True, null=True)
    volume_fc_n = models.DecimalField(db_column='Volume_FC_N', max_digits=18, decimal_places=2, blank=True, null=True)
    tradedate_d = models.DateField(db_column='TradeDate_D')
    valuedate_d = models.DateField(db_column='ValueDate_D', blank=True, null=True)
    create_user = models.ForeignKey(User, models.DO_NOTHING, db_column='Create_User_ID', related_name='transaction_create_user', blank=True, null=True)
    nominal_value_bond_n = models.DecimalField(db_column='Nominal_Value_Bond_N', max_digits=18, decimal_places=2, blank=True, null=True)
    original_input_user = models.ForeignKey(User, models.DO_NOTHING, db_column='Original_Input_User_ID', related_name='transaction_original_input_user', blank=True, null=True)
    
    class Meta:
        managed = False
        db_table = 'Transaction'