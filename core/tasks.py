from agendas.models import Agendamentos
from core.essenciais import EstadoAgendamento
from celery import shared_task

@shared_task
def setar_inicio_agendamento(agendamento_id):
    agendamento: Agendamentos = Agendamentos.carregar(agendamento_id)

    if agendamento.estado_atual == EstadoAgendamento.A_SER_REALIZADO.name:
        agendamento.estado_atual = EstadoAgendamento.FAZENDO
        agendamento.save()

@shared_task
def setar_fim_agendamento(agendamento_id):
    agendamento: Agendamentos = Agendamentos.carregar(agendamento_id)

    if agendamento.estado_atual == EstadoAgendamento.FAZENDO.name:
        agendamento.estado_atual = EstadoAgendamento.ESPERANDO_CONFIRMACAO
        agendamento.save()