'''
Created on 30.11.2016

@author: Moustafa Shama
'''

from django.utils.translation import ugettext_lazy as _

from django import forms

from PortfolioPositionManagement.models import Mandate, Position, Transaction,\
    Investment, Type, Status
from InstrumentDataManagement.models import Currency
from UserManagement.models import Group


class newMandateForm(forms.ModelForm):
    class Meta:
        model = Mandate
        fields = ('name_c',)
        labels = {
            'name_c': _('Name:'),
        }
        widgets = {
            'name_c': forms.TextInput(attrs={ 'required': 'true' }),
        }
        
class positionForm(forms.ModelForm):
    
    class Meta:
        model = Position
        
        fields = ('status', 'quantity_n', 'price_cost_n', 'price_valuation_kvg_n', 'currency',)
        
class newTransactionForm(forms.ModelForm):
    parent_investment = forms.ModelChoiceField(queryset=Investment.objects.exclude(portfolio__isnull=True), label='Parent Investment')
    investment = forms.ModelChoiceField(queryset=Investment.objects.exclude(instrument__isnull=True), label='Investment')
    type = forms.ModelChoiceField(queryset=Type.objects.all(), label='Type')
    status = forms.ModelChoiceField(queryset=Status.objects.all(), label='Status')
    quantity_n = forms.DecimalField(max_digits=30, decimal_places=10, label='Quantity')
    price_n = forms.DecimalField(max_digits=30, decimal_places=10, label='Price')
    currency = forms.ModelChoiceField(queryset=Currency.objects.all(), label='Currency')
    exchangerate_n = forms.DecimalField(max_digits=30, decimal_places=10, label='Exchange rate')
    tradedate_d = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'type':'date',
                                    'class':'trade-date'
                                }))
    valuedate_d = forms.DateField(widget=forms.TextInput(attrs=
                                {
                                    'type':'date'
                                }))
    original_input_usergroup = forms.ModelChoiceField(queryset=Group.objects.all(), label='Currency')
    
    
    class Meta:
        model = Transaction
        fields = ('parent_investment', 'investment', 'type', 'status', 'quantity_n', 'price_n', 'currency', 'exchangerate_n', 'tradedate_d', 'valuedate_d', 'original_input_usergroup')
        
class editTransactionForm(forms.ModelForm):
    
    class Meta:
        model = Transaction
        
        fields = ('status', 'type', 'quantity_n', 'price_n', 'currency', 'exchangerate_n')