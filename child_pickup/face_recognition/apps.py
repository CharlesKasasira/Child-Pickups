from django.apps import AppConfig


class FaceRecognitionConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'face_recognition'

    def ready(self):
        from .scheduler import schedule_trainer
        schedule_trainer()
