from django.apps import AppConfig

class LocaisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'locais'

    def ready(self):
        # Importa o arquivo onde os decoradores @receiver estão
        import locais.models.PredioSetor