from django.contrib import admin

from agendas.models import Agendamentos, TecnicosTIAgendamentos


# Register your models here.
@admin.register(Agendamentos)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('agendamento_id', 'inicio', 'fim', 'data', 'estado_atual', 'sala')

@admin.register(TecnicosTIAgendamentos)
class TecnicoTIAgendamentoAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'agendamento')
