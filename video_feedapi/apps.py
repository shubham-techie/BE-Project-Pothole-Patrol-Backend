from django.apps import AppConfig


class VideoFeedapiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'video_feedapi'

    def ready(self):
        import video_feedapi.signals
