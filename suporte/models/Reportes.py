from django.db import models
from ativos.models.Equipamentos import Equipamentos
from contas.models.Usuarios import Usuarios
from core.essenciais.EstadoReporte import EstadoReporte


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