from django.shortcuts import render, redirect
from RiskModelManagement.models import Riskfactor, Riskfactor_Mapping,\
    RiskfactorComposition
from InstrumentDataManagement.models import Instrument, Marketdatatype
from PortfolioPositionManagement.models import Mandate
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


def viewRiskfactors(request):
    if request.method == 'GET':
        riskfactors = Riskfactor.objects.all()        
        context = {
                   'riskfactors': riskfactors,
                   }
        return render(request, 'RiskModelManagement/viewRiskfactors.html', context)
    
def editRiskfactorMapping(request, riskfactor_id=None):
    if request.method == 'POST':
        parent_riskfactor = Riskfactor.objects.get(pk=riskfactor_id)
        hedge_instrument = Instrument.objects.get(pk=request.POST['riskfactorhedgeinstrument'])
        parent_riskfactor.hedgeinstrument = hedge_instrument
        parent_riskfactor.save()
    return redirect('RiskModelManagement:viewRiskfactor', riskfactor_id=riskfactor_id)

def editRiskfactorComposition(request, riskfactor_id=None):
    if request.method == 'POST':
        parent_riskfactor = Riskfactor.objects.get(pk=riskfactor_id)
        
        current_composition = RiskfactorComposition.objects.filter(riskfactor=parent_riskfactor)
        for composition_element in current_composition:
            composition_element.delete()
                
        for instrument_id in request.POST.getlist('instrument_mapping_list[]'):
            reference_instrument = Instrument.objects.get(pk=instrument_id)
            mandate = Mandate.objects.get(pk=request.POST['mandate'])
            Riskfactor_Mapping(
                               reference_instrument=reference_instrument,
                               riskfactor=parent_riskfactor,
                               mandate=mandate,
                               ).save()
    return redirect('RiskModelManagement:viewRiskfactor', riskfactor_id=riskfactor_id)

def editRiskfactor(request, riskfactor_id=None):
    if request.method == 'POST':
        parent_riskfactor = Riskfactor.objects.get(pk=riskfactor_id)
        if "replaceMapping" in request.POST:
            current_mapping = Riskfactor_Mapping.objects.filter(riskfactor=parent_riskfactor)
            for mapping_element in current_mapping:
                mapping_element.delete()
                
        for instrument_id in request.POST.getlist('instrument_mapping_list[]'):
            reference_instrument = Instrument.objects.get(pk=instrument_id)
            mandate = Mandate.objects.get(pk=request.POST['mandate'])
            Riskfactor_Mapping(
                               reference_instrument=reference_instrument,
                               riskfactor=parent_riskfactor,
                               mandate=mandate,
                               ).save()
    return redirect('RiskModelManagement:viewRiskfactor', riskfactor_id=riskfactor_id)
    
def viewRiskfactor(request, riskfactor_id=None):
    if request.method == 'POST' and 'riskfactorList' in request.POST:
        selectedRiskfactor = request.POST['riskfactorList']
    elif request.method == 'GET' and riskfactor_id:
        selectedRiskfactor = riskfactor_id
    else:
        return redirect('RiskModelManagement:viewRiskfactors')
    
    riskfactor = Riskfactor.objects.get(pk=selectedRiskfactor)
    try:
        riskfactor_mapping = Riskfactor_Mapping.objects.filter(riskfactor=riskfactor)
    except ObjectDoesNotExist:
        riskfactor_mapping = None
        
    try:
        riskfactor_composition = RiskfactorComposition.objects.filter(parent_riskfactor=riskfactor)
    except ObjectDoesNotExist:
        riskfactor_composition = None
        
    hedge_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Derivative'])
    mapping_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Equity','Fixed_Income','Derivative'])
    index_list = Instrument.objects.filter(marketdatatype__type_c__in=['Index','Currency'])
    riskfactors = Riskfactor.objects.all()
    mandates = Mandate.objects.all()
    
    context = {                 
               'mapping_instrument_list': mapping_instrument_list,
               'hedge_instrument_list': hedge_instrument_list,
               'index_list': index_list,
               'riskfactors': riskfactors,
               'mandates': mandates,
               
               'riskfactor': riskfactor,
               'riskfactor_mapping': riskfactor_mapping,
               'riskfactor_composition': riskfactor_composition,
               }
    return render(request, 'RiskModelManagement/viewRiskfactor.html', context)

def addRiskfactor(request):
    if request.method == 'GET':
        hedge_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Derivative'])
        mapping_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Equity','Fixed_Income','Derivative'])
        index_list = Instrument.objects.filter(marketdatatype__type_c__in=['Index','Currency'])
        riskfactors = Riskfactor.objects.all()
        mandates = Mandate.objects.all()
        
        context = {
                   'mapping_instrument_list': mapping_instrument_list,
                   'hedge_instrument_list': hedge_instrument_list,
                   'index_list': index_list,
                   'riskfactors': riskfactors,
                   'mandates': mandates,
                }
        return render(request, 'RiskModelManagement/addRiskfactor.html', context)
    elif request.method == 'POST':
        riskfactor_instrument = Instrument.objects.get(pk=request.POST['riskfactorinstrument']) 
        if request.POST['riskfactorhedgeinstrument']:
            hedge_instrument = Instrument.objects.get(pk=request.POST['riskfactorhedgeinstrument'])
        else:
            hedge_instrument = None
            
        parent_riskfactor = Riskfactor(riskfactorinstrument=riskfactor_instrument, hedgeinstrument=hedge_instrument)
        parent_riskfactor.save()
        
        if ('has_composition' in request.POST) and len(request.POST.getlist('riskfactor[]')) > 0:
            for riskfactor_id,weight in zip(request.POST.getlist('riskfactor[]'), request.POST.getlist('weight[]')):
                if riskfactor_id:
                    riskfactor_element = Riskfactor.objects.get(pk=riskfactor_id)
                    RiskfactorComposition(
                                          parent_riskfactor=parent_riskfactor,
                                          riskfactor=riskfactor_element,
                                          weight_n=weight,
                                          ).save()
        
        if ('has_mapping' in request.POST) and request.POST['instrument_mapping_list[]']:
            for instrument_id in request.POST.getlist('instrument_mapping_list[]'):
                reference_instrument = Instrument.objects.get(pk=instrument_id)
                mandate = Mandate.objects.get(pk=request.POST['mandate'])
                Riskfactor_Mapping(
                                   reference_instrument=reference_instrument,
                                   riskfactor=parent_riskfactor,
                                   mandate=mandate,
                                   ).save()
        
        successMessage = 'Risk factor is saved successfully'
        
        hedge_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Derivative'])
        mapping_instrument_list = Instrument.objects.filter(marketdatatype__type_c__in=['Equity','Fixed_Income','Derivative'])
        index_list = Instrument.objects.filter(marketdatatype__type_c__in=['Index','Currency'])
        riskfactors = Riskfactor.objects.all()
        mandates = Mandate.objects.all()
        
        context = { 
                   'successMessage': successMessage,                  
                   'mapping_instrument_list': mapping_instrument_list,
                   'hedge_instrument_list': hedge_instrument_list,
                   'index_list': index_list,
                   'riskfactors': riskfactors,
                   'mandates': mandates,
                }
        return render(request, 'RiskModelManagement/addRiskfactor.html', context)