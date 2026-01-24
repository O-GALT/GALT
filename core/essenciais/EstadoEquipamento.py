from django.db import models

class EstadoEquipamento(models.TextChoices):
    FUNCIONANDO = 'FUNCIONANDO', "Funcionando"
    MANUTENCAO = 'MANUTENCAO', "Manutencao"
    DEFEITUOSO = 'DEFEITUOSO', "Defeituoso"
    ALERTA = 'ALERTA', 'Alerta'