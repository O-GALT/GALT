from django.db import models
from . Equipamentos import Equipamentos

class HistoricoManutencoes(models.Model):
    historico_manutencoes_id = models.AutoField(primary_key=True)
    equipamento = models.OneToOneField(Equipamentos, on_delete=models.CASCADE, null=False, related_name='historico_manutencoes')
    titulo = models.CharField(null=False, blank=False, max_length=20)
    data = models.DateField(null=False, auto_now_add=True)

    class Meta:
        verbose_name = 'Historico de Manutencoes'
        verbose_name_plural = 'Historicos de Manutencoes'

    def __str__(self):
        return f"{self.titulo} ({self.equipamento.tipo} {self.equipamento.serial})"
