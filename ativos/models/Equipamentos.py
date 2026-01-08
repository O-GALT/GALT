from django.db import models
from core.essenciais import EstadoEquipamento, TipoEquipamento
from locais.models.Salas import Salas


class Equipamentos(models.Model):
    equipamento_id = models.AutoField(primary_key=True)
    sala = models.ForeignKey(Salas, on_delete=models.CASCADE, null=False, related_name='equipamentos')
    posicao = models.IntegerField(null=False, blank=False)
    tipo = models.TextField(null=False, blank=False, choices=TipoEquipamento.choices)
    serial = models.CharField(null=False, unique=True, max_length=13)
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoEquipamento.choices, default=EstadoEquipamento.FUNCIONANDO, max_length=50)
    fabricante = models.CharField(null=False, blank=False, max_length=100)
    data_aquisicao = models.DateField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['posicao', 'sala'], name='u_posicao_sala')
        ]
        verbose_name = 'Equipamentos'
        verbose_name_plural = 'Equipamentos'

    def __srt__(self):
        return f'{self.tipo} / {self.serial}'