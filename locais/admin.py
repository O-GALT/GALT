from django.contrib import admin

from locais.models import Predio, Setor, PredioSetor, Sala

# Register your models here.
@admin.register(Predio)
class PredioAdmin(admin.ModelAdmin):
    list_display = ('predio_id', 'predio')

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    list_display = ('setor_id', 'setor')

@admin.register(PredioSetor)
class PredioSetorAdmin(admin.ModelAdmin):
    list_display = ('predio', 'setor')

@admin.register(Sala)
class SalaAdmin(admin.ModelAdmin):
    list_display = ('sala_id', 'numero', 'estado_sala', 'localizacao', 'predio_setor')