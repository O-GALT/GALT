from django.db import models
from . Equipamento import Equipamento

class HistoricoManutencoes(models.Model):
    historico_manutencoes_id = models.AutoField(primary_key=True)
    titulo = models.CharField(null=False, blank=False, max_length=20)
    data = models.DateField(null=False, auto_now_add=True)
    equipamento = models.OneToOneField(Equipamento, on_delete=models.CASCADE, null=False, related_name='historico_manutencoes')

    class Meta:
        verbose_name = 'Historico de Manutencoes'
        verbose_name_plural = 'Historicos de Manutencoes'

    def __str__(self):
        return f"{self.titulo} ({self.equipamento.tipo} {self.equipamento.serial})"
