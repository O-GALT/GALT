from django.db import models

class Acao(models.TextChoices):
    CRIAR_EQUIPAMENTO = 'CRIAR_EQUIPAMENTO', "Criar equipamento"
    CRIAR_SALA = 'CRIAR_SALA', "Criar sala"
    CRIAR_PREDIO = 'CRIAR_PREDIO', "Criar predio"
    CRIAR_SETOR = 'CRIAR_SETOR', "Criar setor"
    CRIAR_AGENDAMENTO = 'CRIAR_AGENDAMENTO', "Criar agendamento"
    CRIAR_USUARIO = 'CRIAR_USUARIO', "Criar usuario"

    ATUALIZAR_EQUIPAMENTO = 'ATUALIZAR_EQUIPAMENTO', "Atualizar equipamento"
    ATUALIZAR_SALA = 'ATUALIZAR_SALA', "Atualizar sala"
    ATUALIZAR_PREDIO = 'ATUALIZAR_PREDIO', "Atualizar predio"
    ATUALIZAR_SETOR = 'ATUALIZAR_SETOR', "Atualizar setor"
    ATUALIZAR_AGENDAMENTO = 'ATUALIZAR_AGENDAMENTO', "Atualizar agendamento"
    ATUALIZAR_USUARIO = 'ATUALIZAR_USUARIO', "Atualizar usuario"

    DELETAR_EQUIPAMENTO = 'DELETAR_EQUIPAMENTO', "Deletar equipamento"
    DELETAR_SALA = 'DELETAR_SALA', "Deletar sala"
    DELETAR_PREDIO = 'DELETAR_PREDIO', "Deletar predio"
    DELETAR_SETOR = 'DELETAR_SETOR', "Deletar setor"
    DELETAR_AGENDAMENTO = 'DELETAR_AGENDAMENTO', "Deletar agendamento"
    DELETAR_USUARIO = 'DELETAR_USUARIO', "Deletar usuario"


    ABRIR_REPORTE = 'ABRIR_REPORTE', "Abrir reporte"
    TROCAR_EQUIPAMENTO_SALA = 'TROCAR_EQUIPAMENTO_SALA', "Trocar equipamento sala"