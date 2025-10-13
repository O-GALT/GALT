from django.db import models
from . Predio import  Predio
from . Setor import Setor

class PredioSetor(models.Model):
    predio = models.ForeignKey(Predio, on_delete= models.CASCADE, null=False, related_name='predios_setores')
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE, null=False, related_name='predios_setores')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['predio', 'setor'], name='u_predio_setor')
        ]
        verbose_name = 'Predio e setor'
        verbose_name_plural = 'Predios e setors'

    def __str__(self):
        return f'{self.predio} / {self.setor}'