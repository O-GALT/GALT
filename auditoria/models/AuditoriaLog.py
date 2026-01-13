from django.db import models
from contas.models.Usuarios import Usuarios
from core.essenciais import Acao, TipoAlvo


class AuditoriaLog(models.Model):
    auditoria_id = models.AutoField(primary_key=True)
    usuario = models.ForeignKey(Usuarios, on_delete=models.SET_NULL, null=True, related_name='auditorias')
    acao = models.TextField(null=False, blank=False, choices=Acao.choices)
    data = models.DateField(null=False, auto_now_add=True)
    alvo_acao = models.TextField(null=False, blank=False, choices=TipoAlvo.choices)

    class Meta:
        verbose_name = 'Log de auditoria'
        verbose_name_plural = 'Logs de auditoria'

    def __str__(self):
        return f"{self.acao} - {self.usuario or 'Usuário desconhecido'} - {self.data.strftime('%d/%m/%Y %H:%M')}"
