from django.contrib.auth.decorators import login_required
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario

from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from core.essenciais import Acao, TipoAlvo
from locais.forms import UsuarioForm, PredioForm, SetorForm, SalaForm, EquipamentoForm
from core.emails.GerenciadorEmails import GerenciadorEmails
from django.contrib.auth import authenticate, login
from core.auditorias.GerenciadorAuditoria import GerenciadorAuditoria


def pagina_login(request):
    if request.method == 'POST':
        user = authenticate(
           request,
           username=request.POST.get('email_escolar'),
           password=request.POST.get('senha')
        )
    
        if user:
            login(request, user)
            next_url = request.POST.get("next")
            if next_url:
                return redirect(next_url)
            else:
               return redirect('locais_predio_detail', 0)
    return render(request, 'core/pages/login.html')

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def concluido_modal(request):
    return render(request, 'core/pages/modais/modal-concluido.html')

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def exclusao_modal(request):
    return render(request, 'core/pages/modais/modal-exclusao.html')

def equipamento_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/equipamento-visao-usuario.html')

@login_required
def report_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/report-equipamento-usuario.html')


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_usuario_modal(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            admin = request.user

            user = form.save(commit=False)
            user.username = user.email_escolar
            user.nome = user.email_escolar
            password = user.password
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            GerenciadorEmails.enviar_email(user.email, user.email_escolar, password, user.groups)
            GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_USUARIO, list(user.groups.all())[0])
            return HttpResponseRedirect(reverse('criar_recursos'))
        else:
            print(form.errors)
            return HttpResponse('error')
    else:
        form = UsuarioForm()
    return render(request, 'core/pages/modais/modal-criar-usuario.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_predio_modal(request):
    form = PredioForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_PREDIO, TipoAlvo.PREDIO)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-predio.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_setor_modal(request):
    form = SetorForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_SETOR, TipoAlvo.SETOR)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-setor.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_sala_modal(request):
    form = SalaForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_SALA, TipoAlvo.SALA)
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-sala.html', {'form': form})

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR])
def criar_equipamento_modal(request):
    form = EquipamentoForm(request.POST or None)
    if form.is_valid():
        admin = request.user
        form.save()
        GerenciadorAuditoria.persistir_auditoria(admin, Acao.CRIAR_EQUIPAMENTO, TipoAlvo(form.cleaned_data['tipo']))
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', {'form': form})