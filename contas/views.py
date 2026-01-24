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
    usuario = request.user

    if request.method == "POST":
        usuario.cpf = request.POST.get("cpf")
        usuario.email = request.POST.get("email")
        usuario.numero = request.POST.get("numero")
        usuario.email_escolar = request.POST.get("email_escolar")
        usuario.save()

    return render(request, 'contas/partials/components_centrais/informacoes_pessoais/informacoes_pessoais.html', {'usuario': usuario})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_recursos(request):
    return render(request,'contas/partials/components_centrais/recursos/recursos.html')