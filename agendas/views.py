from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.http import HttpResponse

from django.contrib.auth.decorators import login_required

from agendas.essenciais.format_agendamentos import formatar_agendamento
from agendas.models import TecnicosTIAgendamentos, Agendamentos
from auditoria.models import AuditoriaLog
from contas.models import TecnicosTI
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.essenciais import TipoUsuario, Acao, TipoAlvo, EstadoAgendamento
from core.schedule.jobs import Jobs
from locais.models import Salas
import json


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def index(request):
    context = {}
    user = request.user
    user_id = user.id

    is_admin = user.groups.filter(
        name=TipoUsuario.ADMINISTRADOR.value
    ).exists()

    is_tecnico = user.groups.filter(
        name=TipoUsuario.TECNICO_TI.value
    ).exists()


    if is_admin:
        lista_agendamentos_pendentes = Agendamentos.carregar_by_estado(
            EstadoAgendamento.A_SER_REALIZADO
        )
        lista_agendamentos_fazendo = Agendamentos.carregar_by_estado(
            EstadoAgendamento.FAZENDO
        )
        lista_agendamentos_feedback = Agendamentos.carregar_by_estado(
            EstadoAgendamento.ESPERANDO_CONFIRMACAO
        )
        lista_agendamentos_inacabado = Agendamentos.carregar_by_estado(
            EstadoAgendamento.INACABADO
        )
        lista_agendamentos_feito = Agendamentos.carregar_by_estado(
            EstadoAgendamento.FEITO
        )

    elif is_tecnico:
        lista_agendamentos_pendentes = Agendamentos.carregar_by_estado_and_tecnico_id(
            EstadoAgendamento.A_SER_REALIZADO, user_id
        )
        lista_agendamentos_fazendo = Agendamentos.carregar_by_estado_and_tecnico_id(
            EstadoAgendamento.FAZENDO, user_id
        )
        lista_agendamentos_feedback = Agendamentos.carregar_by_estado_and_tecnico_id(
            EstadoAgendamento.ESPERANDO_CONFIRMACAO, user_id
        )
        lista_agendamentos_inacabado = Agendamentos.carregar_by_estado_and_tecnico_id(
            EstadoAgendamento.INACABADO, user_id
        )
        lista_agendamentos_feito = Agendamentos.carregar_by_estado_and_tecnico_id(
            EstadoAgendamento.FEITO, user_id
        )

    else:
        return redirect('core_login')



    context['pendentes'] = {
        "cards": [formatar_agendamento(a) for a in lista_agendamentos_pendentes],
        "count": len(lista_agendamentos_pendentes),
    }

    context['em_andamento'] = {
        "cards": [formatar_agendamento(a) for a in lista_agendamentos_fazendo],
        "count": len(lista_agendamentos_fazendo),
    }

    context['feedback'] = {
        "cards": [formatar_agendamento(a) for a in lista_agendamentos_feedback],
        "count": len(lista_agendamentos_feedback),
    }

    context['inacabado'] = {
        "cards": [formatar_agendamento(a) for a in lista_agendamentos_inacabado],
        "count": len(lista_agendamentos_inacabado),
    }

    context['finalizado'] = {
        "cards": [formatar_agendamento(a) for a in lista_agendamentos_feito],
        "count": len(lista_agendamentos_feito),
    }

    return render(request,'agendas/pages/kanban/kanban.html',context)


def agendar_manutencao(request):
    next = request.POST['next_url']
    sala_id = request.POST['sala']
    tecnicos_id = request.POST['tecnicos']
    data_manutencao = request.POST['data_manutencao']
    horario_inicio = request.POST['horario_inicio']
    horario_final = request.POST['horario_final']
    descricao = request.POST['descricao']

    if not sala_id or not tecnicos_id or not data_manutencao or not horario_inicio or not horario_final or not descricao:
        return HttpResponseRedirect(next)

    tecnicos_id = list(map(int, json.loads(tecnicos_id)))

    tecnicos = TecnicosTI.objects.filter(usuario_id__in=tecnicos_id)
    sala = Salas.carregar(sala_id)


    agendamento = Agendamentos(
        sala=sala,
        inicio=horario_inicio,
        fim=horario_final,
        data=data_manutencao,
        descricao=descricao
    )

    agendamento.save()

    tecnico_agendamento = None
    tem_responsavel = False
    for tecnico in tecnicos:
        if request.user.id == tecnico.usuario.id:
            tem_responsavel = True
        tecnico_agendamento = TecnicosTIAgendamentos(
            tecnico=tecnico,
            agendamento=agendamento,
            responsavel= True if request.user.id == tecnico.usuario.id else False
        )
        tecnico_agendamento.save()

    if not tem_responsavel:
        tecnico_agendamento.responsavel = True
        tecnico_agendamento.save()

    AuditoriaLog.persistir_auditoria(request.user, Acao.CRIAR_AGENDAMENTO, TipoAlvo.AGENDAMENTO)
    Jobs.setar_comportamento_agendamento_inicio_e_fim(agendamento)
    return HttpResponseRedirect(next)