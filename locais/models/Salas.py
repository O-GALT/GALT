from django.db import models

from core.essenciais import EstadoSala
from locais.models.Setores import Setores


class Salas(models.Model):
    sala_id = models.AutoField(primary_key=True)
    setor = models.ForeignKey(Setores, models.CASCADE, null=False, related_name='salas')
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoSala.choices, default=EstadoSala.LIBERADA, max_length=50)
    localizacao = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = 'Salas'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"Sala {self.localizacao} - {self.setor_id}"
