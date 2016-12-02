from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
from .forms import UploadFileForm
from data_saving.saving_functions import save_in_DB

import pandas as pd



def uploadData(request):
    
    uploadForm = UploadFileForm()
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['file'].name.lower().endswith('.csv'):
                input_data = pd.read_csv(form.cleaned_data['file'])
            elif form.cleaned_data['file'].name.lower().endswith(('.xls', '.xlsx',)):
                input_data = pd.read_excel(form.cleaned_data['file'])
            else:
                context = {
                           'errorMessages': ['file is not valid'],
                           'uploadForm': uploadForm,
                           }
                return render(request, 'ManualUpload/manualUpload.html', context)
            
            message = save_in_DB(input_data, form.cleaned_data['table_name'], form.cleaned_data['with_instrument'])
            context = {
                       'uploadForm': uploadForm,
                       }
            if len(message) == 0:
                context['successMessage'] = 'Data is inserted successfully'
            else:
                context['errorMessages'] = message
        else:
            context = {
                       'errorMessages': ['Please choose a file'],
                       'uploadForm': uploadForm,
                       }
    elif request.method == 'GET':
        context = {
                   'uploadForm': uploadForm,
                   }
    return render(request, 'ManualUpload/manualUpload.html', context)