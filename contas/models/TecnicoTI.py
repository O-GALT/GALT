from django.db import  models
from . Usuario import Usuario

class TecnicoTI(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, primary_key=True, related_name='tecnico')
    manutencoes = models.IntegerField(null=False, default=0)
    cargo = models.CharField(null=False, blank=False, max_length=50)

    class Meta:
        verbose_name = 'Tecnico de TI'
        verbose_name_plural = 'Tecnicos de TI'

    def __str__(self):
        return f"{self.usuario.nome} ({self.cargo})"