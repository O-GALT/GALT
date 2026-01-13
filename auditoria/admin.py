from django.contrib import admin

from auditoria.models import AuditoriaLog
from core.essenciais import TipoAlvo, TipoUsuario


# Register your models here.
@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    list_display = ('auditoria_id', 'tipo_autor', 'usuario', 'acao', 'data', 'alvo_acao')

    def tipo_autor(self, obj):
        grupos = list(obj.usuario.groups.all())
        return TipoUsuario(grupos[0].name).label