'''
Created on 15.09.2016

@author: Moustafa Shama
'''
from django.utils.translation import ugettext_lazy as _

from django import forms

from .models import Currency, Instrument, Codification, Country, Marketdatatype, Market, AssetClass, Instrumentsynonym
from PortfolioPositionManagement.models import Mandate

class newMarketDataTypeForm(forms.ModelForm):
    class Meta:
        model = Marketdatatype
        fields = ('name_c', 'type_c')
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
            'type_c': forms.Select(choices = ([('Stock','Equity'), ('Bond','Bond'),('Derivative','Derivative'), ('InterestRate','InterestRate'), ('Currency','Currency'), ]))
        }
        labels = {
            'name_c': _('Name:'),
            'type_c': _('Choose type:')
        }
        
class newMarketForm(forms.ModelForm):
    class Meta:
        model = Market
        fields = ('iso_code_c', 'name_c', 'denomination_c')
        labels = {
            'iso_code_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        widgets = {
            'iso_code_c': forms.TextInput(attrs={ 'required': 'true' }),
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }
        
class codificationForm(forms.Form):
    codification = forms.ModelChoiceField(label='Code type:', queryset=Codification.objects.all())
    code = forms.CharField(label='Code:', widget=forms.TextInput(attrs={ 'required': 'true' }),)
    
class newCodificationForm(forms.ModelForm):
    class Meta:
        model = Codification
        fields = ('name_c', 'denomination_c')
        labels = {
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }
        
class newAssetClassForm(forms.ModelForm):
    parent_assetclass = forms.ModelChoiceField(queryset=AssetClass.objects.all(), label='Parent asset class:', required=False)
    class Meta:
        model = AssetClass
        fields = ('name_c', 'denomination_c', 'parent_assetclass','level_n')
        labels = {
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
            'parent_assetclass': _('Parent asset class:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
            'level_n': forms.HiddenInput(attrs={ 'value': '0'}),
        }

class instrumentAssetClassMapping(forms.Form):
    instruments = forms.ModelMultipleChoiceField(label='Choose Instruments', queryset=Instrument.objects.all(), widget=forms.SelectMultiple(attrs={'size': 20}),)
    mandate = forms.ModelChoiceField(label='Mandate:', queryset=Mandate.objects.all(), required=True,)
    

class newCurrencyForm(forms.ModelForm):
    class Meta:
        model = Currency
        fields = ('isocode_c', 'name_c', 'denomination_c')
        labels = {
            'isocode_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        widgets = {
            'isocode_c': forms.TextInput(attrs={ 'required': 'true' }),
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }

class newCountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = ('isocode_c', 'name_c', 'denomination_c')
        labels = {
            'isocode_c': _('ISO Code:'),
            'name_c': _('Name:'),
            'denomination_c': _('Denomination:'),
        }
        widgets = {
            'isocode_c': forms.TextInput(attrs={ 'required': 'true' }),
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }

class newInstrumentForm(forms.Form):
    source = forms.ChoiceField(label='Source:',  choices = ([('DS','DataStream'), ('BBG','Bloomberg'), ('ISIN','ISIN'),]),required=True,)
    market = forms.ModelChoiceField(label='Market:', queryset=Market.objects.all(), required=False,)
    marketdatatype = forms.ModelChoiceField(label='Market Data Type:', queryset=Marketdatatype.objects.all())
    currency = forms.ModelChoiceField(label='Currency:', queryset=Currency.objects.all(), required=False,)
    underlyingcurrency = forms.ModelChoiceField(label='Underlying Currency:', queryset=Currency.objects.all(), required=False,)
    country = forms.ModelChoiceField(label='Country:', queryset=Country.objects.all(), required=False,)
    risk_country = forms.ModelChoiceField(label='Risk Country:', queryset=Country.objects.all(), required=False,)
    names = forms.CharField(label='Instruments:', widget=forms.Textarea)

class instrumentSearchForm(forms.Form):
    source = forms.ChoiceField(label='Source:',  choices = ([('DS','DataStream'), ('BBG','Bloomberg'), ('ISIN','ISIN'),]),required=True,)
    marketdatatype = forms.ModelChoiceField(label='Market Data Type:', queryset=Marketdatatype.objects.all(), required=False,)
    names = forms.CharField(label='Instruments:', widget=forms.Textarea)
    market = forms.ModelChoiceField(label='Market:', queryset=Market.objects.all(), required=False,)
    
class newInstrumentSynonymForm(forms.Form):
    codification = forms.ModelChoiceField(label='Code type:', queryset=Codification.objects.all())
    code_c = forms.CharField(label='Code:')
    instrument = forms.CharField(label='Instrument', widget=forms.HiddenInput)