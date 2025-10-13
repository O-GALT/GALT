from django.db import  models

class Predio(models.Model):
    predio_id = models.AutoField(primary_key=True)
    predio = models.CharField(null=False, blank=False, unique=True, max_length=50)

    class Meta:
        verbose_name = 'Predio'
        verbose_name_plural = 'Predios'

    def __str__(self):
        return self.predio