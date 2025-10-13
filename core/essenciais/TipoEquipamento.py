from django.db import models

class TipoEquipamento(models.TextChoices):
    PROJETOR = 'PROJETOR', 'Projetor'
    COMPUTADOR = 'COMPUTADOR', 'Computador'
    AR_CONDICIONADO = 'AR_CONDICIONADO', 'Ar condicionado'
