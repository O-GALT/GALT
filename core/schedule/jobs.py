from datetime import date, time

from django.utils import timezone
from django_celery_beat.models import ClockedSchedule, PeriodicTask
import json

from agendas.models import Agendamentos


class Jobs:
    @staticmethod
    def setar_comportamento_agendamento_inicio_e_fim(agendamento: Agendamentos):
        PeriodicTask.objects.create(
            name=f'agendamento.inicio.{agendamento.agendamento_id}',
            task=f'core.tasks.setar_inicio_agendamento',
            one_off=True,
            clocked=Jobs.retornar_clocked_schedule(agendamento, agendamento.inicio),
            args=json.dumps([agendamento.agendamento_id])

        )

        PeriodicTask.objects.create(
            name=f'agendamento.fim.{agendamento.agendamento_id}',
            task=f'core.tasks.setar_fim_agendamento',
            one_off=True,
            clocked=Jobs.retornar_clocked_schedule(agendamento, agendamento.fim),
            args = json.dumps([agendamento.agendamento_id])
        )

    @staticmethod
    def retornar_clocked_schedule(agendamento: Agendamentos, horario):
        horario_agendamento_timezone = timezone.make_aware(
            timezone.datetime.combine(
                date.fromisoformat(agendamento.data),
                time.fromisoformat(horario)
            )
        )
        return ClockedSchedule.objects.create(clocked_time=horario_agendamento_timezone)