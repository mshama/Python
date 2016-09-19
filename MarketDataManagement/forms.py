'''
Created on 15.09.2016

@author: Moustafa Shama
'''
from django.utils.translation import ugettext_lazy as _

from django import forms

from _datetime import datetime

from .models import MarketDataField_Mapping,GoldenRecordField,DatasourceField,Marketdatatype

class newFieldMappingForm(forms.ModelForm):
    class Meta:
        model = MarketDataField_Mapping
        fields = ('goldenrecord_field', 'datasource_field', 'marketdatatype', 'valid_from', 'valid_to')
        labels = {
            'iso_code_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        
    goldenrecord_field = forms.ModelChoiceField(queryset=GoldenRecordField.objects.all())
    datasource_field = forms.ModelChoiceField(queryset=DatasourceField.objects.all())
    marketdatatype = forms.ModelChoiceField(queryset=Marketdatatype.objects.all())
    valid_from = forms.DateField(initial=datetime.now().date())
    valid_to = forms.DateField(initial=datetime.now().date())