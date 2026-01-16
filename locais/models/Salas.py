from django.db import models

from core.essenciais import EstadoSala
from locais.models.Setores import Setores
from django.db.models import Count

class Salas(models.Model):
    sala_id = models.AutoField(primary_key=True)
    setor = models.ForeignKey(Setores, models.CASCADE, null=False, blank=False, related_name='salas')
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoSala.choices, default=EstadoSala.LIBERADA, max_length=50)
    localizacao = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = 'Salas'
        verbose_name_plural = 'Salas'

    def __str__(self):
        return f"Sala {self.localizacao} - {self.setor.setor} - {self.setor.predio.predio}"

    @staticmethod
    def listar_salas_com_equipamentos_mais_defeituoso_predio(predio_id):
        return Salas.objects.filter(equipamentos__sala__setor__predio__predio_id=predio_id, equipamentos__estado_atual='DEFEITUOSO').values('sala_id', 'localizacao').annotate(equipamentos_defeituosos=Count('equipamentos'), necessidade_interditacao=(Count('equipamentos') * 100)/10).order_by('-equipamentos_defeituosos')