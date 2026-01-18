from django.db import models
from django.db.models import F, Count

from locais.models import Predios


class Setores(models.Model):
    setor_id = models.AutoField(primary_key=True)
    predio = models.ForeignKey(Predios, on_delete=models.CASCADE, null=False, blank=False, related_name='setores')
    setor = models.CharField(null=False, blank=False, max_length=100)
    localizacao = models.CharField(null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Setores'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return self.setor

    @staticmethod
    def listar_setores_predio(predio_id):
        return Setores.objects.filter(salas__setor__predio__predio_id=predio_id).values('setor', 'localizacao', predio_nome=F('predio__predio')).annotate(salas=Count('salas'))

    @staticmethod
    def listar_setores_predio_filtro(predio_id):
        return Setores.objects.filter(predio__predio_id=predio_id)