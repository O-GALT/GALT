from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Página de Ativos funcionando!")

def equipamento(request):
    return HttpResponse("Página de equipamentos")

# VIEW QUE CRIEI PARA TESTAR RENDERIZACAO DO HEADER DA PAGINA DE EQUIPAMENTOS(se quiser, pode excluir)
# def equipamento(request):
#     return HttpResponse(render(request, 'ativos/partials/headers/equipamento_header.html'))