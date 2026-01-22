from django.db import models

class Fileira(models.TextChoices):
    FILEIRA_COMPUTADORES_ESQUERDA = 'FILEIRA_COMPUTADORES_ESQUERDA', 'Fileira de computadores a esquerda'
    FILEIRA_COMPUTADORES_DIREITA = 'FILEIRA_COMPUTADORES_DIREITA', 'Fileira de computadores a direita'
    FUNDO = 'FUNDO', 'Fundo'