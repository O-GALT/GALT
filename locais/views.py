from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de locais funcionando!")
    
def salas(request):
    return HttpResponse("Página de salas funcionando!")

def setores(request):
    return HttpResponse("Página de setores funcionando!")

def predios(request):   
    return HttpResponse("Página de prédios funcionando!")