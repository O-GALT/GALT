from django.contrib import admin

from contas.models import TecnicosTI, Usuarios


# Register your models here.
@admin.register(TecnicosTI)
class TecnicoTIAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'cargo')

@admin.register(Usuarios)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'email', 'email_escolar', 'cpf', 'password')
