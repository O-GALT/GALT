from auditoria.models.AuditoriaLog import AuditoriaLog
from contas.models import Usuarios
from core.essenciais import TipoAlvo, Acao

class GerenciadorAuditoria:
    @staticmethod
    def persistir_auditoria(autor: Usuarios, acao:Acao, alvo_acao: TipoAlvo):
        AuditoriaLog.objects.create(
            usuario=autor,
            acao=acao,
            alvo_acao=alvo_acao
        )