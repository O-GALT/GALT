from django.contrib import admin

from ativos.models import Equipamentos, HistoricoManutencoes


# Register your models here.
@admin.register(Equipamentos)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('equipamento_id', 'sala', 'posicao', 'tipo', 'serial', 'estado_equipamento', 'fabricante', 'data_aquisicao')

@admin.register(HistoricoManutencoes)
class HistoricoManutencoesAdmin(admin.ModelAdmin):
    list_display = ('historico_manutencoes_id', 'equipamento', 'titulo', 'data')
