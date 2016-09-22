from django.shortcuts import render
from django.http import HttpResponse,HttpResponseNotFound
from django.db.models import Max
from django.template.context_processors import request
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# build in libraries
import pandas as pd
from _datetime import datetime

# model imports
from .models import MarketDataField_Mapping

# form imports
from .forms import newFieldMappingForm
from InstrumentDataManagement.forms import newMarketDataTypeForm
from MarketDataManagement.forms import newGoldenRecordFieldForm,\
    newDatasourceFieldForm

# Create your views here.
def manageMapping(request, condition=''):
    if request.method == 'GET':
        if condition == 'active':
            marketdatafield_mapping = MarketDataField_Mapping.objects.exclude(valid_to__isnull=False)
        else:
            marketdatafield_mapping = MarketDataField_Mapping.objects.all()
        fieldMappingForm = newFieldMappingForm()
        marketDataTypeForm = newMarketDataTypeForm()
        goldenrecordfieldForm = newGoldenRecordFieldForm()
        datasourcefieldForm = newDatasourceFieldForm()
        context = {
                   'field_mapping': marketdatafield_mapping,
                   'fieldMappingForm': fieldMappingForm,
                   'marketDataTypeForm': marketDataTypeForm,
                   'goldenrecordfieldForm': goldenrecordfieldForm,
                   'datasourcefieldForm': datasourcefieldForm,
        }
        return render(request, 'MarketDataManagement/viewMapping.html', context)