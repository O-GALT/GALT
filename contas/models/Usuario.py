from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    nome = models.CharField(null=False, blank=False, max_length=100)
    email_pessoal = models.CharField(null=False, blank=False, max_length=100)
    email_escolar = models.CharField(null=False, blank=False, max_length=100)
    cpf = models.CharField(null=False, blank=False, max_length=13)
    telefone = models.CharField(null=False, blank=False, max_length=13)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nome
