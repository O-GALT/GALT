from django.http import HttpResponse
from django.shortcuts import render

from ativos.models import Equipamentos
from core.graficos.GeradorGraficos import GeradorGraficos
from locais.models import Salas


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
    context = {}
    context['grafico_saude_predio'] = GeradorGraficos.gerar_grafico_saude_local('setor')
    context['salas'] = [Salas(sala_id=1, localizacao='A13'), Salas(sala_id=2, localizacao='M92'),
                        Salas(sala_id=3, localizacao='A02'), Salas(sala_id=4, localizacao='Z45'),
                        Salas(sala_id=5, localizacao='M92'), Salas(sala_id=6, localizacao='M92'),
                        Salas(sala_id=7, localizacao='M92'), Salas(sala_id=8, localizacao='M92')]
    context['grafico_estado_equipamentos'] = GeradorGraficos.gerar_grafico_estado_equipamentos(261, 170, 69)
    context['grafico_estado_salas'] = GeradorGraficos.gerar_grafico_estado_salas(200, 160, 30)
    context['grafico_reporte_tipo_equipamento'] = GeradorGraficos.gerar_grafico_reports_por_tipo()
    context['objetos'] = [
        {'equipamento_id': '1', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
        {'equipamento_id': '2', 'nome': 'Philips A12', 'tipo': 'Projetor', 'serial': '12301126732',
         'quantidade_manutencoes': '100', 'sala': 'B1'},
        {'equipamento_id': '3', 'nome': 'Joon FK1', 'tipo': 'Computador', 'serial': '744723419211',
         'quantidade_manutencoes': '99', 'sala': '124'},
        {'equipamento_id': '4', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
        {'equipamento_id': '5', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
        {'equipamento_id': '6', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
        {'equipamento_id': '7', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
        {'equipamento_id': '8', 'nome': 'Thunder V12', 'tipo': 'Projetor', 'serial': '19238419213',
         'quantidade_manutencoes': '150', 'sala': 'A34'},
    ]
    return HttpResponse(render(request, 'locais/paginas/setor/setor.html', context))


def predios(request):
    context = {}
    context['grafico_estado_equipamentos'] = GeradorGraficos.gerar_grafico_estado_equipamentos(261, 170, 69)
    context['grafico_estado_salas'] = GeradorGraficos.gerar_grafico_estado_salas(200, 160, 30)
    context['grafico_saude_predio'] = GeradorGraficos.gerar_grafico_saude_local('predio')
    context['grafico_reporte_tipo_equipamento'] = GeradorGraficos.gerar_grafico_reports_por_tipo()
    context['grafico_indice_manutencoes'] = GeradorGraficos.gerar_grafico_indice_manutencoes()
    context['quantidade_tecnicos'] = range(7)
    context['equipamentos'] = [{'equipamento_id':1, 'serial':  '1002', 'manutencoes': 7},
                               {'equipamento_id': 1, 'serial': '1002', 'manutencoes': 7},
                               {'equipamento_id': 1, 'serial': '1002', 'manutencoes': 7},
                               {'equipamento_id': 1, 'serial': '1002', 'manutencoes': 7}
                               ]
    context['salas'] = [{'sala_id':1, 'localizacao':'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'},
                        {'sala_id': 1, 'localizacao': 'A13'}
                        ]
    return HttpResponse(render(request, 'locais/paginas/predio/predio.html', context))


def predios_equipamentos(request):
    context = {}
    context['equipamentos'] = [
        {'classe_estado': 'defeituoso', 'nome_equipamento': 'Thunder V12', 'estado': 'Defeituoso', 'sala': 'A17',
         'posicao': 'A12', 'tipo_equipamento': 'computador'},
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
    return HttpResponse(render(request, 'locais/paginas/predio/equipamento/predio_equipamentos.html', context))


def predios_setores(request):
    context = {
        'setores': [
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
             'quantidade_salas': '12'},
            {'setor': 'Setores administrativo', 'predio': 'Predio principal', 'localizacao': 'Primeiro andar',
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
