from django.db import models

class TipoUsuario(models.TextChoices):
    ADMINISTRADOR = 'ADMINISTRADOR', 'Administrador'
    TECNICO_TI = 'TECNICO_TI', 'Tecnico de TI'
    ALUNO = 'ALUNO', 'Aluno'
    SERVIDOR = 'SERVIDOR', 'Servidor'