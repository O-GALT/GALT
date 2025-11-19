from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de contas funcionando!")

def eu(request):
    return render(request, 'contas/partials/components_centrais/informacoes_pessoais/informacoes_pessoais.html')
# VIEW QUE CRIEI PARA TESTAR A RENDERIZACAO DO HEADER DA PAGINA DE CRIACAO DE RECURSOS(se quiser, pode excluir)
def criar_recursos(request):
    return render(request,'contas/partials/components_centrais/recursos/recursos.html')