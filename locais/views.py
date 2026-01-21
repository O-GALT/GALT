from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from ativos.models import Equipamentos
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario, TipoEquipamento, EstadoEquipamento, EstadoSala
from core.graficos.GeradorGraficos import GeradorGraficos
from core.sql.SQLNativo import SQLNativo
from locais.models import Salas, Setores
from suporte.models import Reportes


# Create your views here.
def home(request):
    return HttpResponse(
        render(request, 'locais/paginas/predio/equipamento'))
        # Implementação temporária, essa view irá retornar outro html que está em desenvolvimento.

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def salas(request, sala_id):
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

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def setores(request, setor_id):
    context = {}
    context['grafico_saude_predio'] = GeradorGraficos.gerar_grafico_saude_local('setor', 100)
    context['salas'] = [{'sala_id': 1, 'localizacao': 'A13', 'necessidade_interditacao': '80', 'equipamentos_defeituosos': '10', 'equipamentos': '20'}]
    context['grafico_estado_equipamentos'] = GeradorGraficos.gerar_grafico_estado_equipamentos(261, 170, 69)
    context['grafico_estado_salas'] = GeradorGraficos.gerar_grafico_estado_salas(200, 160, 30)
    context['grafico_reporte_tipo_equipamento'] = GeradorGraficos.gerar_grafico_reports_por_tipo(None)
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


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def predios(request, predio_id):
    indicadores_predio = SQLNativo.carregar_indicadores_predio(predio_id)[0]

    resultado = SQLNativo.listar_equipamentos_mais_defeituosos_predio(predio_id)
    context = {}
    context['predio_id'] = indicadores_predio['predio_id']
    context['nome_predio'] = indicadores_predio['predio']
    context['total_salas'] = indicadores_predio['total_salas']
    context['total_equipamentos'] = indicadores_predio['total_equipamentos']
    context['total_setores'] = indicadores_predio['total_setores']
    context['reportes_abertos'] = indicadores_predio['reportes_abertos']
    context['manutencoes_hoje'] = indicadores_predio['manutencoes_hoje']
    context['salas_precisam_cuidados'] = indicadores_predio['salas_inapta']
    context['manutencoes_pendentes'] = indicadores_predio['manutencoes_pendentes']
    context['grafico_estado_equipamentos'] = GeradorGraficos.gerar_grafico_estado_equipamentos(indicadores_predio['equipamentos_funcionando'], indicadores_predio['equipamentos_manutencao'], indicadores_predio['equipamentos_defeituoso'])
    context['grafico_estado_salas'] = GeradorGraficos.gerar_grafico_estado_salas(indicadores_predio['salas_liberada'], indicadores_predio['salas_manutencao'], indicadores_predio['salas_inapta'])
    context['grafico_saude_predio'] = GeradorGraficos.gerar_grafico_saude_local('predio', indicadores_predio['saude_predio'])
    context['grafico_reporte_tipo_equipamento'] = GeradorGraficos.gerar_grafico_reports_por_tipo(Reportes.carregar_reportes_durante_a_semana_do_predio(predio_id))
    context['grafico_indice_manutencoes'] = GeradorGraficos.gerar_grafico_indice_manutencoes()
    context['quantidade_tecnicos'] = range(7)
    context['equipamentos'] = [{'equipamento_id':equipamento['equipamento_id'], 'serial': equipamento['serial'], 'manutencoes': equipamento['manutencoes'], 'necessidade_substituicao': equipamento['necessidade_substituicao']} for equipamento in SQLNativo.listar_equipamentos_mais_defeituosos_predio(predio_id)]
    context['salas'] = [{'sala_id':sala['sala_id'], 'localizacao':sala['localizacao'], 'necessidade_interditacao':sala['necessidade_interditacao'], 'equipamentos_defeituosos':sala['equipamentos_defeituosos']} for sala in Salas.listar_salas_com_equipamentos_mais_defeituoso_predio(predio_id)]

    return HttpResponse(render(request, 'locais/paginas/predio/predio.html', context))


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def predios_equipamentos(request, predio_id):
    setor = request.GET.get('setor')
    sala = request.GET.get('sala')
    estado = request.GET.get('estado')

    if setor and sala and estado:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado':equipamento.estado_atual.lower(), 'nome_equipamento':equipamento.serial, 'estado':EstadoEquipamento(equipamento.estado_atual).label, 'sala':equipamento.sala.localizacao,'posicao':equipamento.posicao, 'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_setor_sala_estado(setor, sala, EstadoEquipamento(estado))]
    elif setor and sala:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_setor_sala(setor, sala)]
    elif setor and estado:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label, 'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao, 'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_setor_estado(setor, EstadoEquipamento(estado))]
    elif sala and estado:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_sala_estado(sala, EstadoEquipamento(estado))]
    elif setor:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_setor(setor)]
    elif sala:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_sala(sala)]
    elif estado:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_por_estado(EstadoEquipamento(estado))]
    else:
        equipamentos = [{'equipamento_id': equipamento.equipamento_id, 'classe_estado': equipamento.estado_atual.lower(), 'nome_equipamento': equipamento.serial,'estado': EstadoEquipamento(equipamento.estado_atual).label,'sala': equipamento.sala.localizacao, 'posicao': equipamento.posicao,'tipo_equipamento': TipoEquipamento(equipamento.tipo).label} for equipamento in Equipamentos.listar_equipamentos_do_predio(predio_id)]

    info_predio = SQLNativo.carregar_nome_salas_equipamentos_setores_predio(predio_id)[0]
    context = {}
    context['predio_id'] = info_predio['predio_id']
    context['nome_predio'] = info_predio['predio']
    context['total_salas'] = info_predio['total_salas']
    context['total_equipamentos'] = info_predio['total_equipamentos']
    context['total_setores'] = info_predio['total_setores']
    context['setores'] = [{'input': str(setor.setor_id), 'output': setor.setor} for setor in Setores.listar_setores_predio_filtro(predio_id)]
    context['salas'] = [{'input': str(sala.sala_id), 'output': 'Sala ' + sala.localizacao} for sala in Salas.listar_salas_predio(predio_id)]
    context['equipamentos'] = equipamentos
    context['estados'] = [{'input': estado.name, 'output': estado.label} for estado in [tipo_estado for tipo_estado in EstadoEquipamento]]

    return HttpResponse(render(request, 'locais/paginas/predio/equipamento/predio_equipamentos.html', context))


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def predios_setores(request, predio_id):
    info_predio = SQLNativo.carregar_nome_salas_equipamentos_setores_predio(predio_id)[0]
    context = {}
    context['predio_id'] = info_predio['predio_id']
    context['nome_predio'] = info_predio['predio']
    context['total_salas'] = info_predio['total_salas']
    context['total_equipamentos'] = info_predio['total_equipamentos']
    context['total_setores'] = info_predio['total_setores']
    context['setores'] = [{'setor': setor['setor'], 'predio': setor['predio_nome'], 'localizacao': setor['localizacao'],'quantidade_salas': setor['salas']} for setor in Setores.listar_setores_predio(predio_id)]
    return HttpResponse(render(request, 'locais/paginas/predio/setor/predio_setores.html', context))

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def predios_salas(request, predio_id):
    setor = request.GET.get('setor')
    estado = request.GET.get('estado')

    if setor and estado:
        salas = [{'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_setor_estado(setor, EstadoSala(estado))]

    elif setor:
        salas = [{'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_setor(setor)]

    elif estado:
        salas = [{'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_estado(EstadoSala(estado))]
    else:
        salas = [{'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_salas_predio(predio_id)]

    info_predio = SQLNativo.carregar_nome_salas_equipamentos_setores_predio(predio_id)[0]
    context = {}
    context['predio_id'] = info_predio ['predio_id']
    context['nome_predio'] = info_predio ['predio']
    context['total_salas'] = info_predio ['total_salas']
    context['total_equipamentos'] = info_predio ['total_equipamentos']
    context['total_setores'] = info_predio ['total_setores']
    context['salas'] = salas
    context['setores'] = [{'input': str(setor.setor_id), 'output': setor.setor} for setor in Setores.listar_setores_predio_filtro(predio_id)]
    context['estados'] = [{'input': estado.name, 'output': estado.label} for estado in[tipo_estado for tipo_estado in EstadoSala]]
    return HttpResponse(render(request, 'locais/paginas/predio/sala/predio_salas.html', context))
