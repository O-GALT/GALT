from django.db import models

class Acao(models.TextChoices):
    CRIAR_EQUIPAMENTO = 'CRIAR_EQUIPAMENTO', "Criar equipamento"
    ATUALIZAR_EQUIPAMENTO = 'ATUALIZAR_EQUIPAMENTO', "Atualizar equipamento"
    DELETAR_EQUIPAMENTO = 'DELETAR_EQUIPAMENTO', "Deletar equipamento"

    CRIAR_SALA = 'CRIAR_SALA', "Criar sala"
    ATUALIZAR_SALA = 'ATUALIZAR_SALA', "Atualizar sala"
    DELETAR_SALA = 'DELETAR_SALA', "Deletar sala"

    CRIAR_PREDIO = 'CRIAR_PREDIO', "Criar predio"
    ATUALIZAR_PREDIO = 'ATUALIZAR_PREDIO', "Atualizar predio"
    DELETAR_PREDIO = 'DELETAR_PREDIO', "Deletar predio"

    CRIAR_SETOR = 'CRIAR_SETOR', "Criar setor"
    ATUALIZAR_SETOR = 'ATUALIZAR_SETOR', "Atualizar setor"
    DELETAR_SETOR = 'DELETAR_SETOR', "Deletar setor"

    CRIAR_AGENDAMENTO = 'CRIAR_AGENDAMENTO', "Criar agendamento"
    ATUALIZAR_AGENDAMENTO = 'ATUALIZAR_AGENDAMENTO', "Atualizar agendamento"
    DELETAR_AGENDAMENTO = 'DELETAR_AGENDAMENTO', "Deletar agendamento"

    CRIAR_USUARIO = 'CRIAR_USUARIO', "Criar usuario"
    ATUALIZAR_USUARIO = 'ATUALIZAR_USUARIO', "Atualizar usuario"
    DELETAR_USUARIO = 'DELETAR_USUARIO', "Deletar usuario"

    ABRIR_REPORTE = 'ABRIR_REPORTE', "Abrir reporte"
    TROCAR_EQUIPAMENTO_SALA = 'TROCAR_EQUIPAMENTO_SALA', "Trocar equipamento sala"