from django.db import models
from django.contrib.auth.models import User
from core.methods import file_uploader


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    picture = models.ImageField(upload_to=file_uploader)

    def __str__(self):
        return self.user.username
