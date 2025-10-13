from django.db import models
from . Agendamento import Agendamento
from contas.models.TecnicoTI import TecnicoTI

class TecnicoTIAgendamento(models.Model):
    tecnico = models.ForeignKey(TecnicoTI, on_delete=models.CASCADE, null=False, related_name='agendamentos_tecnicos')
    agendamento = models.ForeignKey(Agendamento, on_delete=models.CASCADE, null=False, related_name='agendamentos_tecnicos')

    class Meta:
        verbose_name = 'TecnicoTI e Agendamento'
        verbose_name_plural = 'TécnicosTI e agendamentos'