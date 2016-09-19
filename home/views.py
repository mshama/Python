from django.shortcuts import render

# Create your views here.
def index(request):
    request.session.flush()
    
    context = {
               'homeText': 'This is Homepage',
               }
    return render(request, 'home/index.html', context)