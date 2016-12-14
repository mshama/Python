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
    name_c = models.CharField(db_column='Name_C', max_length=50, null=True)
    riskfactorinstrument = models.ForeignKey(Instrument, on_delete=models.CASCADE , db_column='RiskfactorInsturment_ID', related_name='riskfactor_instrument')
    hedgeinstrument = models.ForeignKey(Instrument, on_delete=models.CASCADE , db_column='HedgeInstrument_ID', related_name='hedge_instrument', blank=True, null=True)
    
    def __str__(self):
        return self.riskfactorinstrument.name_c
    
    class Meta:
        #managed = False
        db_table = 'Riskfactor'
        
        
class RiskfactorComposition(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    parent_riskfactor = models.ForeignKey(Riskfactor, on_delete=models.CASCADE, db_column='Parent_Riskfactor_ID', related_name='composition_reference_riskfactor')
    riskfactor = models.ForeignKey(Riskfactor, on_delete=models.CASCADE, db_column='Riskfactor_ID', related_name='composition_riskfactor')
    weight_n = models.DecimalField(db_column='Weight_N', max_digits=6, decimal_places=4)
    
    class Meta:
        managed = False
        db_table = 'RiskfactorComposition'
        
from PortfolioPositionManagement.models import Mandate
        
class Riskfactor_Mapping(models.Model):
    id = id = models.AutoField(db_column='ID', primary_key=True)
    reference_instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE , db_column='Reference_Instrument_ID', related_name='mapping_reference_instrument')
    mandate = models.ForeignKey(Mandate, on_delete=models.CASCADE, db_column='Mandate_ID')
    riskfactor = models.ForeignKey(Riskfactor, on_delete=models.CASCADE, db_column='Riskfactor_ID', related_name='mapping_riskfactor')
    
    class Meta:
        managed = False
        db_table = 'Riskfactor_Mapping'
        

        
class Lookback(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    value = models.IntegerField(db_column='Value')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Lookback'   
        
class Persistence(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Persistence'  
        
class Confidence(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Confidence'
        
class HoldingTime(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=3)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoldingTime'  

class Riskrawdata(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    creation_dt = models.DateTimeField(db_column='Creation_DT')  # Field name made lowercase.
    riskfactor = models.ForeignKey(Riskfactor, on_delete=models.CASCADE, db_column='Riskfactor_ID')  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', max_length=10)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=30)  # Field name made lowercase.
    value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=3)  # Field name made lowercase.
    lookback = models.ForeignKey(Lookback, on_delete=models.CASCADE, db_column='Lookback_ID')  # Field name made lowercase.
    persistence = models.ForeignKey(Persistence, on_delete=models.CASCADE, db_column='Persistence_ID')  # Field name made lowercase.
    confidence = models.ForeignKey(Confidence, on_delete=models.CASCADE, db_column='Confidence_ID')  # Field name made lowercase.
    holdingtime = models.ForeignKey(HoldingTime, on_delete=models.CASCADE, db_column='HoldingTime_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Riskrawdata'
        
class Sensitivity_C(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    date_d = models.CharField(db_column='Date_D', max_length=10)  # Field name made lowercase.
    creation_dt = models.DateTimeField(db_column='Creation_DT')  # Field name made lowercase.
    riskfactor_mapping_id = models.IntegerField(db_column='Riskfactor_Mapping_ID')  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    value = models.DecimalField(db_column='Value', max_digits=18, decimal_places=3)  # Field name made lowercase.
    lookback = models.ForeignKey(Lookback, on_delete=models.CASCADE, db_column='Lookback_ID')  # Field name made lowercase.
    persistence = models.ForeignKey(Persistence, on_delete=models.CASCADE, db_column='Persistence_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Sensitivity_C'