from django.db import models

from core.essenciais import EstadoAgendamento
from locais.models.Sala import Sala

class Agendamento(models.Model):
    agendamento_id = models.AutoField(primary_key=True)
    inicio = models.TimeField(null=False)
    fim = models.TimeField(null=False)
    data = models.DateField(null=False)
    estado_agendamento = models.CharField(null=False, blank=False, choices=EstadoAgendamento.choices, default=EstadoAgendamento.A_SER_REALIZADO, max_length=40)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=False, related_name='agendamentos')

    class Meta:
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f"{self.data} - {self.sala} ({self.estado_agendamento})"