from django.db import models
from contas.models.Usuarios import Usuarios
from core.essenciais import Acao, TipoAlvo, TipoUsuario


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

    @staticmethod
    def persistir_auditoria(usuario: Usuarios, acao:Acao, alvo_acao:TipoAlvo):
        AuditoriaLog.objects.create(
            usuario=usuario,
            acao=acao,
            alvo_acao=alvo_acao
        )

    @staticmethod
    def listar_auditorias():
        return AuditoriaLog.objects.all()

    @staticmethod
    def listar_por_tipo_autor(tipo_autor:TipoUsuario):
        return AuditoriaLog.objects.filter(usuario__groups__name=tipo_autor.name)

    @staticmethod
    def listar_por_email_escolar(email_escolar):
        return AuditoriaLog.objects.filter(usuario__email_escolar=email_escolar)

    @staticmethod
    def listar_por_acao(acao:Acao):
        return AuditoriaLog.objects.filter(acao=acao.name)

    @staticmethod
    def listar_por_alvo_acao(alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(alvo_acao=alvo.name)

    @staticmethod
    def listar_por_tipo_autor_email_escolar(tipo_autor:TipoUsuario, email_escolar):
        return AuditoriaLog.objects.filter(usuario__groups__name=tipo_autor.name, usuario__email_escolar=email_escolar)

    @staticmethod
    def listar_por_tipo_autor_email_escolar_acao(tipo_autor:TipoUsuario, email_escolar, acao:Acao):
        return AuditoriaLog.objects.filter(usuario__groups__name=tipo_autor.name, usuario__email_escolar=email_escolar, acao=acao.name)

    @staticmethod
    def listar_por_tipo_autor_email_escolar_acao_alvo(tipo_autor:TipoUsuario, email_escolar, acao:Acao, alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(usuario__groups__name=tipo_autor.name, usuario__email_escolar=email_escolar, acao=acao.name, alvo_acao=alvo.name)

    @staticmethod
    def listar_por_email_escolar_acao(email_escolar, acao:Acao):
        return AuditoriaLog.objects.filter(usuario__email_escolar=email_escolar, acao=acao.name)

    @staticmethod
    def listar_por_email_escolar_acao_alvo(email_escolar, acao:Acao, alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(usuario__email_escolar=email_escolar, acao=acao.name, alvo_acao=alvo.name)

    @staticmethod
    def listar_acao_alvo(acao:Acao, alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(acao=acao.name, alvo_acao=alvo.name)

    @staticmethod
    def listar_por_email_escolar_alvo(email_escolar, alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(usuario__email_escolar=email_escolar, alvo_acao=alvo.name)

    @staticmethod
    def listar_por_tipo_autor_alvo(tipo_autor:TipoUsuario, alvo:TipoAlvo):
        return AuditoriaLog.objects.filter(usuario__groups__name=tipo_autor.name, alvo_acao=alvo.name)

