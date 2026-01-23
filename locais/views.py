from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

from ativos.models import Equipamentos
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario, TipoEquipamento, EstadoEquipamento, EstadoSala, Fileira
from core.graficos.GeradorGraficos import GeradorGraficos
from core.sql.SQLNativo import SQLNativo
from locais.models import Salas, Setores
from suporte.models import Reportes


# Create your views here.
def home(request):
    return HttpResponse(
        render(request, 'locais/paginas/predio/equipamento'))
        # Implementação temporária, essa view irá retornar outro html que está em desenvolvimento.

def organizar_equipamentos_sala(lista_equipamentos):
    lista_equipamentos_organizados = []

    if len(lista_equipamentos) > 0:
        i = 0
        equipamento_anterior = lista_equipamentos[0]
        while i < len(lista_equipamentos) and i + 1 <=len(lista_equipamentos):
            if i == 0:
                posicoes_para_chegar_1 = lista_equipamentos[i].posicao - 1
                if posicoes_para_chegar_1 > 0:
                    for interador in range(posicoes_para_chegar_1):
                        lista_equipamentos_organizados.append({'classe_estado': 'posicao-vaga'})
                lista_equipamentos_organizados.append({'equipamento_id': lista_equipamentos[0].equipamento_id, 'classe_estado': lista_equipamentos[0].estado_atual.lower(),'nome_equipamento': lista_equipamentos[0].serial,'estado': EstadoEquipamento(lista_equipamentos[0].estado_atual).label,'sala': lista_equipamentos[0].sala.localizacao,'posicao': lista_equipamentos[0].posicao,'tipo_equipamento': TipoEquipamento(lista_equipamentos[0].tipo).label})
                i = i + 1
                continue

            posicoes_para_chegar_ao_lado_do_equipamento_anterior = (lista_equipamentos[i].posicao - equipamento_anterior.posicao) - 1
            if posicoes_para_chegar_ao_lado_do_equipamento_anterior > 0:
                for interador in range(posicoes_para_chegar_ao_lado_do_equipamento_anterior):
                    lista_equipamentos_organizados.append({'classe_estado': 'posicao-vaga'})
            lista_equipamentos_organizados.append({'equipamento_id': lista_equipamentos[i].equipamento_id, 'classe_estado': lista_equipamentos[i].estado_atual.lower(),'nome_equipamento': lista_equipamentos[i].serial,'estado': EstadoEquipamento(lista_equipamentos[i].estado_atual).label,'sala': lista_equipamentos[i].sala.localizacao,'posicao': lista_equipamentos[i].posicao,'tipo_equipamento': TipoEquipamento(lista_equipamentos[i].tipo).label})
            equipamento_anterior = lista_equipamentos[i]
            i = i + 1
        return lista_equipamentos_organizados

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def salas(request, sala_id):
    equipamentos = Equipamentos.listar_equipamentos_da_sala(sala_id)

    equipamentos_esquerda = []
    equipamentos_direita = []
    equipamentos_fundo = []


    for equipamento in equipamentos:
        if equipamento.fileira ==  Fileira.FILEIRA_COMPUTADORES_ESQUERDA:
            equipamentos_esquerda.append(equipamento)

        if equipamento.fileira ==  Fileira.FILEIRA_COMPUTADORES_DIREITA:
            equipamentos_direita.append(equipamento)

        if equipamento.fileira == Fileira.FUNDO:
            equipamentos_fundo.append(equipamento)

    equipamentos_esquerda_mapeado = organizar_equipamentos_sala(equipamentos_esquerda)
    equipamentos_direita_mapeado = organizar_equipamentos_sala(equipamentos_direita)
    equipamentos_fundo_mapeado = organizar_equipamentos_sala(equipamentos_fundo)

    indicadores_sala = SQLNativo.carregar_indicadores_sala(sala_id)[0]
    context = {
        'qr_code_url': 'locais_sala_detail,' + str(sala_id),
        'localizacao': indicadores_sala['localizacao'],
        'estado_atual_classe': EstadoSala(indicadores_sala['estado_atual']).name,
        'estado_atual': EstadoSala(indicadores_sala['estado_atual']).label,
        'responsavel_manutencao': indicadores_sala['responsavel_manutencao'],
        'computadores': indicadores_sala['computadores'],
        'projetores': indicadores_sala['projetores'],
        'ar_condicionados': indicadores_sala['ar_condicionados'],
        'equipamentos_esquerda': equipamentos_esquerda_mapeado,
        'equipamentos_direita': equipamentos_direita_mapeado,
        'equipamentos_auxiliares': equipamentos_fundo_mapeado
    }
    return render(request, 'locais/paginas/sala/sala.html', context)

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def setores(request, setor_id):
    indicadores_setor = SQLNativo.carregar_indicadores_setor(setor_id)[0]

    context = {}
    context['nome_setor'] = indicadores_setor['setor']
    context['salas_total'] = indicadores_setor['salas_total']
    context['equipamentos_total'] = indicadores_setor['equipamentos_total']
    context['reportes_total'] = indicadores_setor['reportes_total']
    context['salas'] = [{'sala_id': sala['sala_id'], 'localizacao': sala['localizacao'], 'necessidade_interditacao': sala['necessidade_interditacao'], 'equipamentos_defeituosos': sala['equipamentos_defeituosos'], 'equipamentos': '20'} for sala in Salas.listar_salas_com_equipamentos_mais_defeituoso_setor(setor_id)]
    context['grafico_saude_predio'] = GeradorGraficos.gerar_grafico_saude_local('setor', indicadores_setor['nivel_de_saude_setor'])
    context['grafico_estado_equipamentos'] = GeradorGraficos.gerar_grafico_estado_equipamentos(indicadores_setor['equipamentos_funcionando'], indicadores_setor['equipamentos_manutencao'], indicadores_setor['equipamentos_defeituosos'])
    context['grafico_estado_salas'] = GeradorGraficos.gerar_grafico_estado_salas(indicadores_setor['salas_funcionando'], indicadores_setor['salas_manutencao'], indicadores_setor['salas_inaptas'])
    context['grafico_reporte_tipo_equipamento'] = GeradorGraficos.gerar_grafico_reports_por_tipo(Reportes.carregar_reportes_durante_a_semana_do_setor(setor_id))
    context['produtividade_setor'] = indicadores_setor['produtividade_setor']
    context['objetos'] = [{'equipamento_id': equipamento['equipamento_id'], 'nome': equipamento['serial'], 'tipo': equipamento['tipo'], 'serial': '19238419213','quantidade_manutencoes': equipamento['manutencoes'], 'sala': equipamento['sala_localizacao']} for equipamento in Equipamentos.listar_equipamentos_mais_reincidencia_de_falhas_setor(setor_id)]
    context['manutencoes_hoje'] = indicadores_setor['manutencoes_hoje']
    context['manutencoes_agendadas'] = indicadores_setor['manutencoes_agendadas']

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
    context['setores'] = [{'setor_id': setor['setor_id'], 'setor': setor['setor'], 'predio': setor['predio_nome'], 'localizacao': setor['localizacao'],'quantidade_salas': setor['salas']} for setor in Setores.listar_setores_predio(predio_id)]
    return HttpResponse(render(request, 'locais/paginas/predio/setor/predio_setores.html', context))

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def predios_salas(request, predio_id):
    setor = request.GET.get('setor')
    estado = request.GET.get('estado')

    if setor and estado:
        salas = [{'sala_id': sala.sala_id, 'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_setor_estado(setor, EstadoSala(estado))]

    elif setor:
        salas = [{'sala_id': sala.sala_id, 'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_setor(setor)]

    elif estado:
        salas = [{'sala_id': sala.sala_id, 'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_por_estado(EstadoSala(estado))]
    else:
        salas = [{'sala_id': sala.sala_id, 'classe_estado': sala.estado_atual.lower(), 'posicao': sala.localizacao,'estado': EstadoSala(sala.estado_atual).label,'quantidade_projetores': sala.equipamentos.filter(tipo=TipoEquipamento.PROJETOR).count(),'quantidade_computadores': sala.equipamentos.filter(tipo=TipoEquipamento.COMPUTADOR).count(),'quantidade_ar_condicionados': sala.equipamentos.filter(tipo=TipoEquipamento.AR_CONDICIONADO).count()} for sala in Salas.listar_salas_predio(predio_id)]

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
