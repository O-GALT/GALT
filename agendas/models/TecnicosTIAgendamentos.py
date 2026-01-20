from django.db import models
from . Agendamentos import Agendamentos
from contas.models.TecnicosTI import TecnicosTI

class TecnicosTIAgendamentos(models.Model):
    tecnico = models.ForeignKey(TecnicosTI, on_delete=models.CASCADE, null=False, related_name='agendamentos_tecnicos')
    responsavel = models.BooleanField(default=True)
    agendamento = models.ForeignKey(Agendamentos, on_delete=models.CASCADE, null=False, related_name='agendamentos_tecnicos')

    class Meta:
        verbose_name = 'TecnicosTI e Agendamentos'
        verbose_name_plural = 'TécnicosTI e agendamentos'