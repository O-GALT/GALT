from django.db import models

class EstadoSala(models.TextChoices):
    LIBERADA = 'LIBERADA', 'Liberada'
    MANUTENCAO = 'MANUTENCAO', 'Manutenção'
    INAPTA = 'FECHADA', 'Fechada'
