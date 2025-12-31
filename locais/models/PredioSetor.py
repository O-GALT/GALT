from django.db import models
from . Predio import Predio
from . Setor import Setor

from django.db.models.signals import post_save
from django.dispatch import receiver

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

#assim que o predio ou setor eh criado, cria as combinacoes

@receiver(post_save, sender='locais.Predio')
def criar_combinacoes_novo_predio(sender, instance, created, **kwargs):
    print(f"sinal disparado para prédio {instance.predio} (criado: {created})")
    if created:
        from .Setor import Setor 
        from .PredioSetor import PredioSetor
        setores = Setor.objects.all()
        for s in setores:
            PredioSetor.objects.get_or_create(predio=instance, setor=s)

@receiver(post_save, sender='locais.Setor')
def criar_combinacoes_novo_setor(sender, instance, created, **kwargs):
    if created:
        from .Predio import Predio
        from .PredioSetor import PredioSetor
        predios = Predio.objects.all()
        for p in predios:
            PredioSetor.objects.get_or_create(predio=p, setor=instance)
