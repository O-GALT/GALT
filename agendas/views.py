from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Página de Agendas funcionando!")

def kanban(request):
    return render(request, 'agendas/partials/kanban/kanban.html')