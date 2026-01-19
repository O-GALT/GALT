from django.db import models

from contas.models import TecnicosTI
from core.essenciais import EstadoAgendamento
from . Equipamentos import Equipamentos
from django.db.models.functions import ExtractMonth
from django.db.models import Count
from django.db.models import F

class HistoricoManutencoes(models.Model):
    historico_manutencoes_id = models.AutoField(primary_key=True)
    equipamento = models.ForeignKey(Equipamentos, on_delete=models.CASCADE, null=False, related_name='historico_manutencoes')
    tecnico = models.ForeignKey(TecnicosTI, on_delete=models.CASCADE, null=False, related_name='historico_manutencoes')
    titulo = models.CharField(null=False, blank=False, max_length=20)
    data = models.DateField(null=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Historico de Manutencoes'
        verbose_name_plural = 'Historicos de Manutencoes'

    def __str__(self):
        return f"{self.titulo} ({self.equipamento.tipo} {self.equipamento.serial})"

    @staticmethod
    def listar_manutencoes_no_predio_durante_o_ano(predio_id):
        return HistoricoManutencoes.objects.filter(equipamento__sala__setor__predio__predio_id=predio_id).annotate(mes=ExtractMonth('data')).values(mes=F('mes')).annotate(manutencoes=Count('*'))

    @staticmethod
    def listar_historico_equipamento(equipamento_id):
        return HistoricoManutencoes.objects.filter(equipamento__equipamento_id=equipamento_id).values('historico_manutencoes_id', 'titulo', 'data', responsavel=F('tecnico__usuario__email_escolar')).order_by('historico_manutencoes_id')
