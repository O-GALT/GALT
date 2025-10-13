from django.contrib import admin

from contas.models import TecnicoTI, Usuario


# Register your models here.
@admin.register(TecnicoTI)
class TecnicoTIAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'manutencoes', 'cargo')

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email_pessoal', 'email_escolar', 'cpf', 'telefone')
