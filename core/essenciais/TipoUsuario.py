from django.db import models

class TipoUsuario(models.TextChoices):
    PROFESSOR = 'PROFESSOR', 'Professor'
    ALUNO = 'ALUNO', 'Aluno'
    TECNICO_TI = 'TECNICO_TI', 'Tecnico de TI'
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    ROOT = 'ROOT', 'Root'