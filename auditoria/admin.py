from django.contrib import admin

from auditoria.models import AuditoriaLog


# Register your models here.
@admin.register(AuditoriaLog)
class AuditoriaLogAdmin(admin.ModelAdmin):
    list_display = ('auditoria_id', 'acao', 'alvo_id', 'tipo_alvo', 'data', 'user')