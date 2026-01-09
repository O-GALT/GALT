from django.contrib import admin

from locais.models import Predios, Setores, Salas


# Register your models here.
@admin.register(Predios)
class PredioAdmin(admin.ModelAdmin):
    list_display = ('predio_id', 'predio')

@admin.register(Setores)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('setor_id', 'predio', 'setor', 'localizacao')

@admin.register(Salas)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('sala_id', 'setor', 'estado_atual', 'localizacao')