from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

# Create your views here.

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def index(request):
    return render(request, 'agendas/partials/kanban/kanban.html')