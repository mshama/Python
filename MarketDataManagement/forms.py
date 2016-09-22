'''
Created on 15.09.2016

@author: Moustafa Shama
'''
from django.utils.translation import ugettext_lazy as _

from django import forms

from _datetime import datetime

from .models import MarketDataField_Mapping,GoldenRecordField,DatasourceField,Marketdatatype


class newGoldenRecordFieldForm(forms.ModelForm):
    class Meta:
        model = GoldenRecordField
        fields = ('name_c',)
        labels = {
            'name_c': _('Field Name:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }

class newDatasourceFieldForm(forms.ModelForm):
    class Meta:
        model = DatasourceField
        fields = ('name_c','data_source_c',)
        labels = {
            'name_c': _('Field Name:'),
            'data_source_c': _('Datasource:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
            'data_source_c': forms.Select(choices = ([('DS','DataStream'), ('BBG','Bloomberg'), ]))
        }
        

class newFieldMappingForm(forms.ModelForm):
    class Meta:
        model = MarketDataField_Mapping
        fields = ('goldenrecord_field', 'datasource_field', 'marketdatatype', 'valid_from', 'valid_to',)
        labels = {
            'iso_code_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        
    goldenrecord_field = forms.ModelChoiceField(queryset=GoldenRecordField.objects.all())
    datasource_field = forms.ModelChoiceField(queryset=DatasourceField.objects.all())
    marketdatatype = forms.ModelChoiceField(queryset=Marketdatatype.objects.all())
    valid_from = forms.DateField(initial=datetime.now().date(), widget=forms.TextInput(attrs={ 'required': 'true' }),)
    valid_to = forms.DateField(initial=datetime.now().date(), required=False)