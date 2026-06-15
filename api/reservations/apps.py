from django.apps import AppConfig


class ReservationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api.reservations'

    def ready(self):
            import api.reservations.signals
