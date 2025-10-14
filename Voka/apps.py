from django.apps import AppConfig


class VokaConfig(AppConfig):
    verbose_name = 'Сайт Voka'
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Voka'
    
    def ready(self):    
        import Voka.translation