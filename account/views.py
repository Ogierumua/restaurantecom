

from django.shortcuts import HttpResponse, render

def test(request):
    
    return render(request, 'home.html')


def home(request):
    
    return render(request, 'home.html')

# Create your views here.

