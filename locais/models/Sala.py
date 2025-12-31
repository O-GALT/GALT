from django.db import models

from core.essenciais import EstadoSala
from . import PredioSetor

class Sala(models.Model):
    sala_id = models.AutoField(primary_key=True) 
    numero = models.IntegerField(null=False, blank=False, max_length=10)
    estado_sala = models.CharField(null=False, blank=False, choices=EstadoSala.choices, default=EstadoSala.LIBERADA, max_length=40)
    localizacao = models.CharField(null=False, blank=False, max_length=20)
    predio_setor = models.ForeignKey(PredioSetor, on_delete=models.CASCADE, null=False, related_name='salas')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['predio_setor', 'numero'], name='u_predio_numero')
        ]
        verbose_name = 'Sala'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"Sala {self.numero} - {self.predio_setor.predio} / {self.predio_setor.setor}"
