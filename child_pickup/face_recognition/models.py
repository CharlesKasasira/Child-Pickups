from django.db import models

class UserProfile(models.Model):
    face_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    image_path = models.CharField(max_length=255)

    def __str__(self):
        return self.name
