from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from locais.forms import UsuarioForm, PredioForm, SetorForm, SalaForm, EquipamentoForm

def login(request):
    return render(request, 'core/pages/login.html')

def criar_equipamento_modal(request):
    context = {
        'salas': ['Salas 101', 'Salas 102', 'Salas 103'],
    }
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', context)

def criar_sala_modal(request):
    context = {
        'setores': ['Setores A', 'Setores B', 'Setores C'],
        'predios' : ['Prédio 1', 'Prédio 2', 'Prédio 3'],
    }
    return render(request, 'core/pages/modais/modal-criar-sala.html', context)

def criar_predio_modal(request):
    context = {
        'setores': ['Setores Administrativo', 'Setores Técnico', 'Setores Acadêmico'],
    }
    return render(request, 'core/pages/modais/modal-criar-predio.html', context)

def criar_setor_modal(request):
    return render(request, 'core/pages/modais/modal-criar-setor.html')

def criar_usuario_modal(request):
    context = {
        'usuarios': ['Administrador', 'Aluno', 'Professor', 'Técnico de TI', 'Root']
    }
    return render(request, 'core/pages/modais/modal-criar-usuario.html', context)

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
            form.save()
            return HttpResponseRedirect(reverse('criar_recursos'))
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