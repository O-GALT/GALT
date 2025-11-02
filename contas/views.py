from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de contas funcionando!")

# VIEW QUE CRIEI PARA TESTAR A RENDERIZACAO DO HEADER DA PAGINA DE CRIACAO DE RECURSOS(se quiser, pode excluir)
# def criar_recursos(request):
#     return HttpResponse(render(request,'contas/partials/headers/criacao_recursos_header.html'))