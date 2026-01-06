from django.db import models

class EstadoReporte(models.TextChoices):
    ABERTO = 'ABERTO', "aberto"
    FECHADO = 'FECHADO', "fechado"