from django.db import models

from core.essenciais import EstadoEquipamento, TipoEquipamento
from locais.models.Sala import Sala


class Equipamento(models.Model):
    equipamento_id = models.AutoField(primary_key=True)
    tipo = models.CharField(null=False, blank=False, choices=TipoEquipamento.choices, max_length=40)
    modelo = models.CharField(null=False, blank=False, max_length=40)
    serial = models.IntegerField(null=False, unique=True)
    posicao = models.CharField(null=False, blank=False, max_length=20)
    estado_equipamento = models.CharField(null=False, blank=False, choices=EstadoEquipamento.choices, default=EstadoEquipamento.FUNCIONANDO, max_length=40)
    manutencoes = models.IntegerField(null=False, default=0)
    sala = models.ForeignKey(Sala, on_delete=models.CASCADE, null=False, related_name='equipamentos')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['posicao', 'sala'], name='u_posicao_sala')
        ]
        verbose_name = 'Equipamento'
        verbose_name_plural = 'Equipamentos'

    def __str__(self):
        return f'{self.tipo} / {self.serial}'