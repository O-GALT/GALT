from django.db import models
from ativos.models.Equipamento import Equipamento
from contas.models.Usuario import Usuario

class Reporte(models.Model):
    reporte_id = models.AutoField(primary_key=True)
    titulo = models.CharField(null=False, blank=False, max_length=40)
    mensagem = models.CharField(null=False, blank=False, max_length=100)
    equipamento = models.ForeignKey(Equipamento, on_delete=models.CASCADE, null=False, related_name='reportes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=False, related_name='reportes')
    data = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['equipamento', 'usuario'], name='u_equipamento_usuario')
        ]
        verbose_name = 'Reporte'
        verbose_name_plural = 'Reportes'

    def __str__(self):
        return f"{self.titulo} ({self.usuario.nome} -> {self.equipamento.tipo})"