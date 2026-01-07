from django.db import  models
from . Usuarios import Usuarios

class TecnicosTI(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True, related_name='tecnico')
    cargo = models.CharField(null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Tecnico de TI'
        verbose_name_plural = 'Tecnicos de TI'

    def __str__(self):
        return f"{self.usuario.nome} ({self.cargo})"