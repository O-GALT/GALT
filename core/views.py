from django.shortcuts import render

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