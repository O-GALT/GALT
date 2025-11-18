from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return HttpResponse(
        render(request, 'locais/partials/headers/sala/sala_header.html'))


def salas(request):
    context = {
        'equipamentos_esquerda': [
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'defeituoso', 'nome_equipamento': 'Brigs V79', 'estado': 'Defeituoso', 'sala': 'A17',
             'posicao': 'A2', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A3', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A4', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'funcionando', 'nome_equipamento': 'Brigs V79', 'estado': 'Funcionando', 'sala': 'A17',
             'posicao': 'A5', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A6', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'alerta-report', 'nome_equipamento': 'Thunder V12', 'estado': 'Alerta', 'sala': 'A17',
             'posicao': 'A7', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A8', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A9', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A10', 'tipo_equipamento': 'computador'},

        ],
        'equipamentos_direita': [
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A11', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'defeituoso', 'nome_equipamento': 'Thunder V12', 'estado': 'Defeituoso', 'sala': 'A17',
             'posicao': 'A12', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A13', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A14', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'funcionando', 'nome_equipamento': 'Maximus V20', 'estado': 'Funcionando', 'sala': 'A17',
             'posicao': 'A15', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A16', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'alerta-report', 'nome_equipamento': 'Maximus V20', 'estado': 'Alerta', 'sala': 'A17',
             'posicao': 'A17', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A18', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A19', 'tipo_equipamento': 'computador'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A20', 'tipo_equipamento': 'computador'},

        ],
        'equipamentos_auxiliares': [
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V20', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'funcionando', 'nome_equipamento': 'Thunder V12', 'estado': 'Funcionando', 'sala': 'A17',
             'posicao': 'A2', 'tipo_equipamento': 'projetor'},
        ]
    }
    return render(request, 'locais/paginas/sala/sala.html', context)


def setores(request):
    return HttpResponse("Página de setores funcionando!")


def predios(request):
    return HttpResponse("Página de prédios funcionando!")


def predios_equipamentos(request):
    context = {
        'equipamentos': [
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'defeituoso', 'nome_equipamento': 'Maximus V12', 'estado': 'Defeituoso', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Maximus V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'funcionando', 'nome_equipamento': 'Maximus V12', 'estado': 'Funcionando', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Thunder V12', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'alerta-report', 'nome_equipamento': 'Thunder V12', 'estado': 'Alerta', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},
            {'classe_estado': 'manutencao', 'nome_equipamento': 'Brigs V79', 'estado': 'Manutenção', 'sala': 'A17',
             'posicao': 'A1', 'tipo_equipamento': 'projetor'},

        ]
    }
    return HttpResponse(render(request, 'locais/paginas/predio/equipamento/predio_equipamentos.html', context))


def predios_setores(request):
    context = {
        'setores': [
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
            {'setor': 'Setor administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
        ]
    }
    return HttpResponse(render(request, 'locais/paginas/predio/setor/predio_setores.html', context))


def predios_salas(request):
    context = {
        'salas': [
            {'classe_estado': 'manutencao', 'posicao': 'A27', 'estado': 'Manutenção', 'quantidade_projetores': '12',
             'quantidade_computadores': '2', 'quantidade_ar_condicionados': '10'},
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
