from django.shortcuts import render

def login(request):
    return render(request, 'core/pages/login.html')

def criar_equipamento_modal(request):
    context = {
        'salas': ['Sala 101', 'Sala 102', 'Sala 103'],
    }
    return render(request, 'core/pages/modais/modal-criar-equipamento.html', context)

def criar_sala_modal(request):
    context = {
        'setores': ['Setor A', 'Setor B', 'Setor C'],
    }
    return render(request, 'core/pages/modais/modal-criar-sala.html', context)

def criar_predio_modal(request):
    context = {
        'setores': ['Setor Administrativo', 'Setor Técnico', 'Setor Acadêmico'],
    }
    return render(request, 'core/pages/modais/modal-criar-predio.html', context)

def criar_usuario_modal(request):
    context = {
        'usuarios': ['Administrador', 'Aluno', 'Professor', 'Técnico de TI', 'Root']
    }
    return render(request, 'core/pages/modais/modal-criar-usuario.html', context)

def concluido_modal(request):
    return render(request, 'core/pages/modais/modal-concluido.html')


def equipamento_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/equipamento-visao-usuario.html')

def report_visao_usuario(request): 
    return render(request, 'core/pages/visao-do-usuario/report-equipamento-usuario.html')