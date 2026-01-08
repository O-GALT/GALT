from django.db import models

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