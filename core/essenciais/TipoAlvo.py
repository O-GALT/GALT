from django.db import models

class TipoAlvo(models.TextChoices):
    PROJETOR = 'PROJETOR', 'projetor'
    COMPUTADOR = 'COMPUTADOR', 'computador'
    AR_CONDICIONADO = 'AR CONDICIONADO', 'ar condicionado'
    SALA = 'SALA', 'sala'
    PREDIO ='PREDIO', 'predio'
    SETOR = 'SETOR', 'setor'
    AGENDAMENTO = 'AGENDAMENTO', 'agendamento'
    ADMINISTRADOR = 'ADMINISTRADOR', 'administrador'
    TECNICO_TI = 'TECNICO_TI', 'tecnico de ti'
    ALUNO = 'ALUNO', 'aluno'
    PROFESSOR = 'PROFESSOR', 'professor'
    ROOT = 'ROOT', 'root'
