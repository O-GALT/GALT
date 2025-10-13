from django.db import models
from contas.models.Usuario import Usuario
from core.essenciais import Acao, TipoAlvo


class AuditoriaLog(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    acao = models.CharField(null=False, blank=False, choices=Acao.choices, max_length=40)
    alvo_id = models.IntegerField(null=False)
    tipo_alvo = models.CharField(null=False, blank=False, choices=TipoAlvo.choices, max_length=40)
    data = models.DateTimeField(null=False, auto_now_add=True)
    user = models.ForeignKey(Usuario, on_delete=models.SET_NULL, null=True, related_name='auditorias')

    class Meta:
        verbose_name = 'Log de auditoria'
        verbose_name_plural = 'Logs de auditoria'

    def __str__(self):
        return f"{self.acao} - {self.user or 'Usuário desconhecido'} - {self.data.strftime('%d/%m/%Y %H:%M')}"
