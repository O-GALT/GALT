from django.contrib import admin

from suporte.models import Reporte

# Register your models here.
@admin.register(Reporte)
class ReporteAdmin(admin.ModelAdmin):
    list_display = ('reporte_id', 'titulo', 'mensagem', 'equipamento', 'usuario', 'data')
