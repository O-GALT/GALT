from django.contrib import admin

from auditoria.models import AuditoriaLog


# Register your models here.
@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    list_display = ('auditoria_id', 'usuario', 'acao', 'data', 'alvo_acao')