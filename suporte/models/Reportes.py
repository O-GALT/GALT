from django.db import models
from ativos.models.Equipamentos import Equipamentos
from contas.models.Usuarios import Usuarios
from core.essenciais.EstadoReporte import EstadoReporte
from django.db.models import Count
from django.db.models import F
from django.db.models.functions import ExtractWeekDay


class Reportes(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    equipamento = models.ForeignKey(Equipamentos, on_delete=models.CASCADE, null=False, related_name='reportes')
    usuario = models.ForeignKey(Usuarios, on_delete=models.CASCADE, null=False, related_name='reportes')
    titulo = models.CharField(null=False, blank=False, max_length=100)
    mensagem = models.CharField(null=False, blank=False, max_length=200)
    estado_atual = models.CharField(null=False, blank=False, choices=EstadoReporte.choices, default=EstadoReporte.ABERTO, max_length=20)
    data = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Reportes'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f"{self.titulo} ({self.usuario.nome} -> {self.equipamento.tipo})"

    @staticmethod
    def carregar_reportes_durante_a_semana_do_predio(predio_id):
        return Reportes.objects.filter(equipamento__sala__setor__predio__predio_id=predio_id).annotate(
            dia=ExtractWeekDay('data')).values(tipo_equipamento=F('equipamento__tipo'), dia=F('dia')).annotate(
            reportes=Count('reporte_id')).order_by('dia', 'tipo_equipamento')