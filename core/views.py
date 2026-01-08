from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from locais.forms import UsuarioForm, PredioForm, SetorForm, SalaForm, EquipamentoForm
from core.emails.GerenciadorEmails import GerenciadorEmails

def login(request):
    return render(request, 'core/pages/login.html')

def concluido_modal(request):
    return render(request, 'core/pages/modais/modal-concluido.html')

def exclusao_modal(request):
    return render(request, 'core/pages/modais/modal-exclusao.html')


def equipamento_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/equipamento-visao-usuario.html')

def report_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/report-equipamento-usuario.html')


def criar_usuario_modal(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.nome = user.email
            password = user.password
            user.set_password(form.cleaned_data['password'])
            user.save()
            form.save_m2m()
            GerenciadorEmails.enviar_email(user.email, user.email_escolar, password, user.groups)
            return HttpResponseRedirect(reverse('criar_recursos'))
        else:
            print(form.errors)
            return HttpResponse('error')
    else:
        form = UsuarioForm()
    return render(request, 'core/pages/modais/modal-criar-usuario.html', {'form': form})

def criar_predio_modal(request):
    form = PredioForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-predio.html', {'form': form})

def criar_setor_modal(request):
    form = SetorForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-setor.html', {'form': form})

def criar_sala_modal(request):
    form = SalaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-sala.html', {'form': form})

def criar_equipamento_modal(request):
    form = EquipamentoForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('criar_recursos'))
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', {'form': form})