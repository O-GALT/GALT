from django.http import HttpResponse
from django.shortcuts import render

from ativos.models import Equipamento


# Create your views here.
def index(request):
    return HttpResponse('funcionando')

def salas(request):
    return HttpResponse("Página de salas funcionando!")

def setores(request):
    return HttpResponse("Página de setores funcionando!")

def predios(request):
    return HttpResponse("Página de prédios funcionando!")

def predios_equipamentos(request):
    context = {
        'equipamentos': [
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2', 'posicao':'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'defeituoso', 'nome_equipamento': 'Thunder V12', 'estado': 'Defeituoso', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'funcionando', 'nome_equipamento': 'Thunder V12', 'estado': 'Funcionando', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'alerta-report', 'nome_equipamento': 'Thunder V12', 'estado': 'Alerta', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'B2',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},

        ]
    }
    return HttpResponse(render(request, 'locais/paginas/predio/equipamento/predio_equipamentos.html', context))

def predios_setores(request):
    context = {
        'setores': [
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar', 'quantidade_salas':'12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
        ]
    }
    return HttpResponse(render(request, 'locais/paginas/predio/setor/predio_setores.html', context))

def predios_salas(request):
    context = {
        'salas': [
            {'classe_estado': 'manutencao', 'posicao': 'A27', 'estado':'Manutenção', 'quantidade_projetores': '12', 'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},
            {'classe_estado': 'manutencao', 'posicao': 'A27', 'estado': 'Manutenção', 'quantidade_projetores': '12',
             'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},
            {'classe_estado': 'inativa', 'posicao': 'A27', 'estado': 'Inativa', 'quantidade_projetores': '12',
             'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},
            {'classe_estado': '', 'posicao': 'A27', 'estado': 'Manutenção', 'quantidade_projetores': '12',
             'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},
            {'classe_estado': 'manutencao', 'posicao': 'A27', 'estado': 'Manutenção', 'quantidade_projetores': '12',
             'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},

        ]
    }
    return HttpResponse(render(request, 'locais/paginas/predio/sala/predio_salas.html', context))

# VIEWS QUE CRIEI PARA TESTAR RENDERIZACAO DE HEADER DAS PAGINAS DE SALAS, SETORES, PREDIOS, E PREDIOS COM SELECAO DE EQUIPAMENTOS E SALAS(se quiser, pode excluir)

# def index(request):
#     return HttpResponse(render(request,
#                                'core/pages/../core/templates/core/partials/partials_do_headers/filtro/filtro.html'))
#
# def salas(request):
#     return HttpResponse(render(request, 'locais/partials/headers/sala/sala_header.html'))
#
# def setores(request):
#     return HttpResponse(render(request, 'locais/partials/headers/setor/setor_header.html/'))
#
# def predios(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_header.html'))
#
# def predios_equipamentos(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_equipamentos_header.html', {'setor': ['Administrativo', 'Acadêmico', 'Técnico'], 'sala': ['A17', 'A13', 'B24', 'C54', 'D2'], 'estado': [EstadoEquipamento.FUNCIONANDO, EstadoEquipamento.MANUTENCAO, EstadoEquipamento.DEFEITUOSO]}))
#
# def predios_salas(request):
#     return HttpResponse(render(request, 'locais/partials/headers/predio/predio_salas_header.html', {'setor': ['Administrativo', 'Acadêmico', 'Técnico'], 'sala': ['A17', 'A13', 'B24', 'C54', 'D2'], 'estado': [EstadoSala.LIBERADA, EstadoSala.MANUTENCAO, EstadoSala.INAPTA]}))