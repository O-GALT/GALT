from django.db import models

from core.essenciais import EstadoAgendamento
from locais.models.Salas import Salas

class Agendamentos(models.Model):
    agendamento_id = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE, null=False, related_name='agendamentos')
    inicio = models.TimeField(null=False)
    fim = models.TimeField(null=False)
    descricao = models.TextField(null=True, blank=True)
    data = models.DateField(null=False)
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoAgendamento.choices, default=EstadoAgendamento.A_SER_REALIZADO, max_length=100)

    class Meta:
        verbose_name = 'Agendamentos'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.data} - {self.sala} ({self.estado_atual})"

    @staticmethod
    def carregar(agendamento_id):
        return Agendamentos.objects.get(agendamento_id=agendamento_id)

    @staticmethod
    def carregar_by_estado(estado):
        return Agendamentos.objects.filter(estado_atual=estado)

    @staticmethod
    def carregar_by_estado_and_tecnico_id(estado, user_id):
        return (
            Agendamentos.objects
            .filter(
                estado_atual=estado,
                agendamentos_tecnicos__tecnico__usuario_id=user_id
            )
            .select_related(
                'sala',
                'sala__setor',
                'sala__setor__predio'
            )
            .prefetch_related(
                'agendamentos_tecnicos',
                'agendamentos_tecnicos__tecnico'
            )
            .distinct()
        )



