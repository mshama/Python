from django.shortcuts import render,redirect
from django.http import HttpResponse

from PortfolioPositionManagement.models import Portfolio, Mandate, Position,\
    Transaction
from UserManagement.models import User, Group

from datetime import datetime
from PortfolioPositionManagement.forms import newMandateForm, positionForm,\
    editTransactionForm, newTransactionForm
from django.forms.formsets import formset_factory

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
        
def viewPositions(request):
    positions = Position.objects.all().order_by('investment__instrument__name_c')
    context = {
               'positions': positions,
               }
    return render(request, 'PortfolioPositionManagement/viewPositions.html', context)

def deletePosition(request, position_id=None):
    if position_id:
        position = Position.objects.get(pk=position_id)
        position.delete()
        
        return redirect('PortfolioPositionManagement:viewPositions')

def editPosition(request, position_id=None):
    if request.method == 'GET' and position_id:
        position = Position.objects.get(pk=position_id)
        editData = {
                    'status': position.status,
                    'quantity_n': position.quantity_n, 
                    'price_cost_n': position.price_cost_n, 
                    'price_valuation_kvg_n': position.price_valuation_kvg_n, 
                    'currency': position.currency,
                    }
        form = positionForm(editData)
        context = {
                   'position': position,
                   'editForm': form,
                   }
        return render(request, 'PortfolioPositionManagement/editPosition.html', context)
    if request.method == 'POST' and position_id:
        form = positionForm(request.POST)
        if form.is_valid():
            position = Position.objects.get(pk=position_id)
            
            position.status = form.cleaned_data['status']
            position.quantity_n = form.cleaned_data['quantity_n']
            position.price_cost_n = form.cleaned_data['price_cost_n']
            position.price_valuation_kvg_n = form.cleaned_data['price_valuation_kvg_n']
            position.currency = form.cleaned_data['currency']
            
            position.save()
            
            return redirect('PortfolioPositionManagement:viewPositions')
        else:
            position = Position.objects.get(pk=position_id)
            editData = {
                        'status': position.status,
                        'quantity_n': position.quantity_n, 
                        'price_cost_n': position.price_cost_n, 
                        'price_valuation_kvg_n': position.price_valuation_kvg_n, 
                        'currency': position.currency,
                        }
            form = positionForm(editData)
            errorMsg = 'there was an error'
            context = {
                       'position': position,
                       'editForm': form,
                       'errorMsg': errorMsg
                       }
            return render(request, 'PortfolioPositionManagement/editPosition.html', context)
    else:
        return redirect('PortfolioPositionManagement:viewPositions')

    
def viewTransactions(request):
    transactions = Transaction.objects.all()
    context = {
               'transactions': transactions,
               }
    return render(request, 'PortfolioPositionManagement/viewTransactions.html', context)

def addTransactions(request):
    TransactionFormSet = formset_factory(newTransactionForm, max_num=10, min_num=1)
    
    if request.method == 'GET':
        # prepare new transaction form
        transaction_formset = TransactionFormSet()
        context = {
                   'transaction_formset': transaction_formset,
                   }
        return render(request, 'PortfolioPositionManagement/addTransactions.html', context)
    if request.method == 'POST':
        # read form data
        transaction_formset = TransactionFormSet(request.POST, request.FILES)
        # check the validity of the transaction form
        if transaction_formset.is_valid():
            for form in transaction_formset.forms:
                # create new transaction
                transaction = form.save(commit=False)
                if request.session['user']:
                    transaction.create_user = request.session['user']
                transaction.createdate_d = datetime.now().date()
                transaction.save()                
            # update positions
            return redirect('PortfolioPositionManagement:viewTransactions')

def editTransaction(request, transaction_id=None):
    if request.method == 'GET' and transaction_id:
        transaction = Transaction.objects.get(pk=transaction_id)
        editData = {
                    'status': transaction.status,
                    'type': transaction.type, 
                    'quantity_n': transaction.quantity_n, 
                    'price_n': transaction.price_n, 
                    'exchangerate_n': transaction.exchangerate_n,
                    'currency': transaction.currency,
                    }
        form = editTransactionForm(editData)
        context = {
                   'transaction': transaction,
                   'editForm': form,
                   }
        return render(request, 'PortfolioPositionManagement/editTransaction.html', context)
    if request.method == 'POST' and transaction_id:
        form = editTransactionForm(request.POST)
        if form.is_valid():
            transaction = Transaction.objects.get(pk=transaction_id)
            
            transaction.status = form.cleaned_data['status']
            transaction.type = form.cleaned_data['type']
            transaction.quantity_n = form.cleaned_data['quantity_n']
            transaction.price_n = form.cleaned_data['price_n']
            transaction.exchangerate_n = form.cleaned_data['exchangerate_n']
            transaction.currency = form.cleaned_data['currency']
            
            transaction.save()
            
            return redirect('PortfolioPositionManagement:viewPositions')
        else:
            transaction = Transaction.objects.get(pk=transaction_id)
            editData = {
                    'status': transaction.status,
                    'type': transaction.type, 
                    'quantity_n': transaction.quantity_n, 
                    'price_n': transaction.price_n, 
                    'exchangerate_n': transaction.exchangerate_n,
                    'currency': transaction.currency,
                    }
            form = editTransactionForm(editData)
            errorMsg = 'there was an error'
            context = {
                       'transaction': transaction,
                       'editForm': form,
                       'errorMsg': errorMsg
                       }
            return render(request, 'PortfolioPositionManagement/editTransaction.html', context)
    else:
        return redirect('PortfolioPositionManagement:viewTransactions')

def deleteTransaction(request, transaction_id=None):
    if transaction_id:
        transaction = Transaction.objects.get(pk=transaction_id)
        transaction.delete()
        
        return redirect('PortfolioPositionManagement:viewTransactions')

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