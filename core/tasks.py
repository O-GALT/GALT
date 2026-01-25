from agendas.models import Agendamentos
from ativos.models import Equipamentos
from core.essenciais import EstadoAgendamento, EstadoEquipamento, EstadoSala
from celery import shared_task

@shared_task
def setar_inicio_agendamento(agendamento_id):
    agendamento: Agendamentos = Agendamentos.carregar(agendamento_id)

    if agendamento.estado_atual == EstadoAgendamento.A_SER_REALIZADO.name:
        equipamentos: list[Equipamentos] = Equipamentos.listar_equipamentos_da_sala(agendamento.sala.sala_id)

        for equipamento in equipamentos:
            if equipamento.estado_atual == EstadoEquipamento.ALERTA or equipamento.estado_atual == EstadoEquipamento.DEFEITUOSO:
                equipamento.estado_atual = EstadoEquipamento.MANUTENCAO
                equipamento.save()

        agendamento.estado_atual = EstadoAgendamento.FAZENDO
        agendamento.save()

@shared_task
def setar_fim_agendamento(agendamento_id):
    agendamento: Agendamentos = Agendamentos.carregar(agendamento_id)

    if agendamento.estado_atual == EstadoAgendamento.FAZENDO.name:
        agendamento.estado_atual = EstadoAgendamento.ESPERANDO_CONFIRMACAO
        agendamento.save()