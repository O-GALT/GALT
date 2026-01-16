from django.db import  models
from . Usuarios import Usuarios
from django.db.models import Count, F

class TecnicosTI(models.Model):
    usuario = models.OneToOneField(Usuarios, on_delete=models.CASCADE, primary_key=True, related_name='tecnico')
    cargo = models.CharField(null=False, blank=False, max_length=100)

    class Meta:
        verbose_name = 'Tecnico de TI'
        verbose_name_plural = 'Tecnicos de TI'

    def __str__(self):
        return f"{self.usuario.nome} ({self.cargo})"

    @staticmethod
    def listar_tecnicos_mais_manutencoes_mes_predio(predio_id):
        return Usuarios.objects.filter(tecnico__agendamentos_tecnicos__agendamento__sala__setor__predio__predio_id=predio_id).values('email_escolar').annotate(manutencoes=Count('*')).order_by('-manutencoes')