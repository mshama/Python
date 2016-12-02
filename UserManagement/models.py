from django.db import models

# Create your models here.

class Function(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Function'

class Function_Profile(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    function = models.ForeignKey(Function, models.DO_NOTHING, db_column='Function_ID')


class Group(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    name_c = models.CharField(db_column='Name_C', max_length=50)
    denomination_c = models.CharField(db_column='Denomination_C', max_length=50)
    Function_Profile = models.ForeignKey(Function_Profile, models.DO_NOTHING, db_column='Function_Profile_ID')
    
    def __str__(self):
        return self.name_c
    
    class Meta:
        managed = False
        db_table = 'Group'
        
class User(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    firstname_c = models.CharField(db_column='FirstName_C', max_length=50)
    lastname_c = models.CharField(db_column='LastName_C', max_length=50)
    windows_login_c = models.CharField(db_column='Windows_Login_C', max_length=50)
    
    def __str__(self):
        return self.lastname_c + ',' + self.firstname_c
    
    def get_email(self):
        return self.windows_login_c + '@quantcapital.de' 
    
    class Meta:
        managed = False
        db_table = 'User'
        
class User_Group(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING, db_column='User_ID')
    group = models.ForeignKey(Group, models.DO_NOTHING, db_column='Group_ID')
    
    def __str__(self):
        return self.user.windows_login_c + ',' + self.group.name_c
    
    class Meta:
        managed = False
        db_table = 'User_Group'
        unique_together = (('user', 'group',),)