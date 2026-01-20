from django.db import models

class TipoAlvo(models.TextChoices):
    PROJETOR = 'PROJETOR', 'Projetor'
    COMPUTADOR = 'COMPUTADOR', 'Computador'
    AR_CONDICIONADO = 'AR_CONDICIONADO', 'Ar condicionado'
    SALA = 'SALA', 'Salas'
    PREDIO ='PREDIO', 'Predio'
    SETOR = 'SETOR', 'Setores'
    AGENDAMENTO = 'AGENDAMENTO', 'Agendamentos'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    TECNICO_TI = 'TECNICO_TI', 'Tecnico de ti'
    ALUNO = 'ALUNO', 'Aluno'
    PROFESSOR = 'PROFESSOR', 'Professor'
    REPORTE = 'REPORTE', 'Reportes'
