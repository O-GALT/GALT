from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Página de contas funcionando!")

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI, TipoUsuario.ALUNO, TipoUsuario.SERVIDOR]) 
def eu(request):
    return render(request, 'contas/partials/components_centrais/informacoes_pessoais/informacoes_pessoais.html')
# VIEW QUE CRIEI PARA TESTAR A RENDERIZACAO DO HEADER DA PAGINA DE CRIACAO DE RECURSOS(se quiser, pode excluir)
@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_recursos(request):
    return render(request,'contas/partials/components_centrais/recursos/recursos.html')