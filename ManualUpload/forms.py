'''
Created on 25.11.2016

@author: Moustafa Shama
'''
from django import forms

class UploadFileForm(forms.Form):
    CHOICES = (
        ('Portfolio', 'Portfolio'),
        ('Position', 'Position'),
        ('Transaction', 'Transaction'),
    )
    table_name = forms.ChoiceField(label = 'Choose table', choices=CHOICES)
    file = forms.FileField(label = '*Choose file:')
    with_instrument = forms.BooleanField(label='**Including instrument', required=False)