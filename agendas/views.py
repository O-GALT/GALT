import threading

from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from agendas.essenciais.format_agendamentos import formatar_agendamento
from agendas.essenciais.formatar_lista_de_equipamentos_concertados import formatar_lista_de_equipamentos_concertados
from agendas.models import TecnicosTIAgendamentos, Agendamentos
from ativos.models import Equipamentos, HistoricoManutencoes
from auditoria.models import AuditoriaLog
from contas.models import TecnicosTI
from core.autorizacao.filtroAutorizacao import nivel_acesso_permitido
from core.emails.GerenciadorEmails import GerenciadorEmails
from core.essenciais import TipoUsuario, Acao, TipoAlvo, EstadoAgendamento, EstadoEquipamento, EstadoSala
from core.essenciais.EstadoReporte import EstadoReporte
from core.schedule.jobs import Jobs
from locais.models import Salas
import json

from suporte.models import Reportes


@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def index(request):
    context = {}
    user = request.user
    user_id = user.id


    lista_agendamentos_feedback_by_user_id = Agendamentos.carregar_by_estado_and_tecnico_id(
        EstadoAgendamento.ESPERANDO_CONFIRMACAO, request.user.id
    )

    if lista_agendamentos_feedback_by_user_id.exists():
        return redirect('reportar_manutencao', user_id=user_id)

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

    context['is_admin'] = request.user.groups.filter(name=TipoUsuario.ADMINISTRADOR.name).exists()

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

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
def reportar_manutencao(request, user_id):
    agendamento = (
        Agendamentos.objects
        .filter(
            estado_atual=EstadoAgendamento.ESPERANDO_CONFIRMACAO,
            agendamentos_tecnicos__tecnico__usuario_id=user_id
        )
        .select_related('sala')
        .order_by('inicio')
        .first()
    )

    if not agendamento:
        return redirect('agendas_index')

    context = {
        'equipamentos': formatar_lista_de_equipamentos_concertados(agendamento.sala.sala_id),
        'agendamento': agendamento,
        'user_id': user_id
    }

    return render(request, 'agendas/pages/finalizar_manutencao/finalizar_manutencao.html', context)

@login_required
@nivel_acesso_permitido([TipoUsuario.ADMINISTRADOR, TipoUsuario.TECNICO_TI])
# @require_POST
def processar_finalizacao_agendamento(request, agendamento_id):
    agendamento = get_object_or_404(
        Agendamentos,
        agendamento_id=agendamento_id
    )

    equipamentos_ids = request.POST.getlist('equipamentos')

    with (transaction.atomic()):

        if equipamentos_ids:
            agendamento.estado_atual = EstadoAgendamento.FEITO

            for eq in Equipamentos.objects.filter(equipamento_id__in=equipamentos_ids):
                eq.estado_atual = EstadoEquipamento.FUNCIONANDO
                eq.save()
                HistoricoManutencoes(
                    equipamento=eq,
                    tecnico=TecnicosTIAgendamentos.carregar_tecnico_responsavel(agendamento_id).tecnico,
                    titulo=agendamento.descricao,
                ).save()

                reportes = Reportes.objects.filter(equipamento__equipamento_id=eq.equipamento_id)

                for reporte in reportes:
                    reporte.estado_atual = EstadoReporte.FECHADO
                    reporte.save()
                    threading.Thread(
                        target=GerenciadorEmails.enviar_email_fechamento_report,
                        args=(reporte.usuario.email, reporte.usuario.email_escolar)
                    ).start()
            Salas.objects.filter(
                sala_id=agendamento.sala.sala_id
            ).update(
                estado_atual=EstadoSala.LIBERADA
            )

        else:
            agendamento.estado_atual = EstadoAgendamento.INACABADO
            Salas.objects.filter(
                sala_id=agendamento.sala.sala_id
            ).update(
                estado_atual=EstadoSala.LIBERADA
            )

        agendamento.save()

    return redirect('agendas_index')
