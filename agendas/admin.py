from django.contrib import admin

from agendas.models import Agendamento, TecnicoTIAgendamento


# Register your models here.
@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('agendamento_id', 'inicio', 'fim', 'data', 'estado_agendamento', 'sala')

@admin.register(TecnicoTIAgendamento)
class TecnicoTIAgendamentoAdmin(admin.ModelAdmin):
    list_display = ('tecnico', 'agendamento')
