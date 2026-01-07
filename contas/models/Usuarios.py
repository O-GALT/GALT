from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuarios(AbstractUser):
    nome = models.CharField(null=False, blank=False, max_length=100)
    email_escolar = models.EmailField(null=False, blank=False, max_length=100)
    cpf = models.CharField(null=False, blank=False, max_length=14)
    numero = models.CharField(null=False, blank=False, max_length=13)

    class Meta:
        verbose_name = 'Usuarios'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nome
