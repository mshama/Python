from django.db import models


from InstrumentDataManagement.models import Instrument

# Create your models here.


class RiskModel(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    description_c = models.CharField(db_column='Description_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'RiskModel'
        
        
class Riskfactor(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    riskfactorinstrument = models.ForeignKey(Instrument, models.DO_NOTHING , db_column='RiskfactorInsturment_ID', related_name='riskfactor_instrument')
    hedgeinstrument = models.ForeignKey(Instrument, models.DO_NOTHING , db_column='HedgeInstrument_ID', related_name='hedge_instrument', blank=True, null=True)
    
    def __str__(self):
        return self.riskfactorinstrument.name_c
    
    class Meta:
        managed = False
        db_table = 'Riskfactor'
        
        
class RiskfactorComposition(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    parent_riskfactor = models.ForeignKey(Riskfactor, models.DO_NOTHING, db_column='Parent_Riskfactor_ID', related_name='composition_reference_riskfactor')
    riskfactor = models.ForeignKey(Riskfactor, models.DO_NOTHING, db_column='Riskfactor_ID', related_name='composition_riskfactor')
    weight_n = models.DecimalField(db_column='Weight_N', max_digits=6, decimal_places=4)
    
    class Meta:
        managed = False
        db_table = 'RiskfactorComposition'
        
from PortfolioPositionManagement.models import Mandate
        
class Riskfactor_Mapping(models.Model):
    id = id = models.AutoField(db_column='ID', primary_key=True)
    reference_instrument = models.ForeignKey(Instrument, models.DO_NOTHING , db_column='Reference_Instrument_ID', related_name='mapping_reference_instrument')
    mandate = models.ForeignKey(Mandate, models.DO_NOTHING, db_column='Mandate_ID')
    riskfactor = models.ForeignKey(Riskfactor, models.DO_NOTHING, db_column='Riskfactor_ID', related_name='mapping_riskfactor')
    
    class Meta:
        managed = False
        db_table = 'Riskfactor_Mapping'
        
