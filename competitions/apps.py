from django.apps import AppConfig


class CompetitionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'competitions'
    
    def ready(self):
        """Import signals when the app is ready"""
        import competitions.signals
