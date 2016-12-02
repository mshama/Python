from django.shortcuts import render, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.forms.models import model_to_dict


from UserManagement.models import User

# Create your views here.
def index(request):
    if 'user' in request.session:
        loginStatus = True
    else:
        request.session.flush()
        loginStatus = False
    context = {
               'loginStatus': loginStatus,
               'homeText': 'This is Homepage',
               }
    return render(request, 'home/index.html', context)


def checkLogin(request):
    try:
        user = User.objects.get(windows_login_c = request.POST['uname'])
        request.session['user'] = model_to_dict(user)
        loginStatus = True
    except ObjectDoesNotExist:
        loginStatus = False
    context = {
               'loginStatus': loginStatus,
               }
    return render(request, 'home/index.html', context)