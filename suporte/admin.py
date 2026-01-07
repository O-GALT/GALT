from django.contrib import admin

from suporte.models import Reportes

# Register your models here.
@admin.register(Reportes)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte_id', 'titulo', 'mensagem', 'equipamento', 'usuario', 'data')
