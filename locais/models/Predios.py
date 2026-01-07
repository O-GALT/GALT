from django.db import models

class Predios(models.Model):
    predio_id = models.AutoField(primary_key=True)
    predio = models.CharField(null=False, blank=False, unique=True, max_length=30)
<<<<<<< HEAD:locais/models/Predios.py
    predio = models.CharField(null=False, blank=False, unique=True, max_length=100)
=======
    predio = models.CharField(null=False, blank=False, unique=True, max_length=30)
>>>>>>> 55402a8 (feat: verificação de senha nativa do AbstractUser):locais/models/Predio.py

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'

    def __str__(self):
        return self.predio