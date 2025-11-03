from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de Auditoria funcionando!")

# VIEW QUE CRIEI PARA TESTAR A RENDERIZACAO DO HEADER DA PAGINA DE AUDITORIA(se quiser, pode excluir)
# def index(request):
#     return HttpResponse(render(request, 'auditoria/partials/headers/auditoria_header.html'))
