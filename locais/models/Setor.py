from django.db import models

class Setor(models.Model):
    setor_id = models.AutoField(primary_key=True)
    setor = models.CharField(null=False, blank=False, unique=True, max_length=30)

    class Meta:
        verbose_name = 'Setor'
        verbose_name_plural = 'Setores'

    def __str__(self):
        return self.setor