from django.db import models

# Create your models here.
class Portfolio(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Portfolio'
    

class Mandate(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    portfolio = models.ForeignKey(Portfolio, models.DO_NOTHING, db_column='Portfolio_ID')
    
    def __str__(self):
        return self.name_c + " - " + self.portfolio.name_c
    
    class Meta:
        managed = False
        db_table = 'Mandate'