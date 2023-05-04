from django.apps import AppConfig


class PotholeGpsapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'pothole_gpsapi'

    def ready(self) -> None:
        import pothole_gpsapi.signals
