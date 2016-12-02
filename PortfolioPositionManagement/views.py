from django.shortcuts import render,redirect
from django.http import HttpResponse

from PortfolioPositionManagement.models import Portfolio, Mandate
from UserManagement.models import User

from datetime import datetime
from PortfolioPositionManagement.forms import newMandateForm

# Create your views here.

def viewMandates(request):
    if request.method == 'GET':
        mandates = Mandate.objects.all()
        mandateForm = newMandateForm()
        context = {
                   'mandates': mandates,
                   'mandateForm': mandateForm,
               }
        return render(request, 'PortfolioPositionManagement/viewMandates.html', context)
    
def addMandate(request):
    if request.method == 'POST':
        form = newMandateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('PortfolioPositionManagement:viewMandates')
        else:
            return HttpResponse('Error Saving Data')

def viewPortfolios(request):
    if request.method == 'GET':
        portfolios = Portfolio.objects.all()        
        context = {
                   'portfolios': portfolios,
                   }
        return render(request, 'PortfolioPositionManagement/viewPortfolios.html', context)
    elif request.method == 'POST' and request.is_ajax():
        changes =  request.POST.getlist('changes[]')
        message = ""
        for change in changes:
            change = change.split(',')
            try:
                portfolio = Portfolio.objects.get(pk=change[0])
                if(change[1] == 'true'):
                    portfolio.activeflag_b = True
                else:
                    portfolio.activeflag_b = False
                portfolio.last_modf_d = datetime.now().date()
                portfolio.last_modf_user = User(**request.session['user'])
                portfolio.save()
            except Exception as e:
                message = message + str(e)
        
        if len(message) == 0:
            message = "1"        

        return HttpResponse(message)
    elif request.method == 'POST' and not request.is_ajax():
        portfolios = Portfolio.objects.all()        
        context = {
                   'portfolios': portfolios,
                   }
        return render(request, 'PortfolioPositionManagement/viewPortfolios.html', context)