from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from contas.forms import PredioForm, SetorForm, PredioSetorForm, SalaForm, EquipamentoForm, UsuarioForm

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

# modais de recursos

def criar_predio_modal(request):
    if request.method == 'POST':
        predio = PredioForm(request.POST)
        if predio.is_valid():
            predio.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
        else:
            print(predio.errors)
    else:
        predio = PredioForm()
    return render(request, 'core/pages/modais/modal-criar-predio.html', {'form': predio})

def criar_setor_modal(request):
    if request.method == 'POST':
        setor = SetorForm(request.POST)
        if setor.is_valid():
            setor.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
    else:
        setor = SetorForm()
    return render(request, 'core/pages/modais/modal-criar-setor.html', {'form': setor})
    
def criar_sala_modal(request):
    if request.method == 'POST':
        sala = SalaForm(request.POST)
        if sala.is_valid():
            sala.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
    else:
        sala = SalaForm()
    return render(request, 'core/pages/modais/modal-criar-sala.html', {'form': sala })

def criar_equipamento_modal(request):
    if request.method == 'POST':
        equipamento = EquipamentoForm(request.POST)
        if equipamento.is_valid():
            equipamento.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
    else:
        equipamento = EquipamentoForm()
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', {'form': equipamento})

def criar_usuario_modal(request):
    if request.method == 'POST':
        usuario = UsuarioForm(request.POST)
        if usuario.is_valid():
            usuario.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
    else:
        usuario = UsuarioForm()
    return render(request, 'core/pages/modais/modal-criar-usuario.html', {'form': usuario})
