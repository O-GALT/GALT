from django.db import models

class TipoAlvo(models.TextChoices):
    PROJETOR = 'PROJETOR', 'Projetor'
    COMPUTADOR = 'COMPUTADOR', 'Computador'
    AR_CONDICIONADO = 'AR CONDICIONADO', 'Ar condicionado'
    SALA = 'SALA', 'Sala'
    PREDIO ='PREDIO', 'Predio'
    SETOR = 'SETOR', 'Setor'
    AGENDAMENTO = 'AGENDAMENTO', 'Agendamento'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    TECNICO_TI = 'TECNICO_TI', 'Tecnico de ti'
    ALUNO = 'ALUNO', 'Aluno'
    PROFESSOR = 'PROFESSOR', 'Professor'
    ROOT = 'ROOT', 'Root',
    REPORTE = 'REPORTE', 'Reporte'
