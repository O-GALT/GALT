from django.db import models

class EstadoSala(models.TextChoices):
    LIBERADA = 'LIBERADA', 'Liberada'
    MANUTENCAO = 'MANUTENCAO', 'Manutencao'
    INAPTA = 'INAPTA', 'Inapta'