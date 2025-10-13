from django.db import models

class EstadoAgendamento(models.TextChoices):
    A_SER_REALIZADO = 'A_SER_REALIZADO', "A ser realizado"
    FAZENDO = 'FAZENDO', "Fazendo"
    ESPERANDO_CONFIRMACAO = 'ESPERANDO_CONFIRMACAO', "Esperando confirmação"
    INACABADO = 'INACABADO', "Inacabado"
    FEITO = 'FEITO', "Feito"