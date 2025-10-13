from django.contrib import admin

from ativos.models import Equipamento, HistoricoManutencoes


# Register your models here.
@admin.register(Equipamento)
class EquipamentoAdmin(admin.ModelAdmin):
    list_display = ('equipamento_id', 'tipo', 'serial', 'posicao', 'estado_equipamento', 'manutencoes', 'sala')

@admin.register(HistoricoManutencoes)
class HistoricoManutencoesAdmin(admin.ModelAdmin):
    list_display = ('historico_manutencoes_id', 'titulo', 'data', 'equipamento')
