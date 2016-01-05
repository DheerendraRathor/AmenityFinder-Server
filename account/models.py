import uuid

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone

from core.methods import file_uploader


class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')
    picture = models.URLField()

    def __str__(self):
        return self.user.username


class UserToken(models.Model):
    user = models.ForeignKey(User)
    token = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(default=timezone.now)
    has_expired = models.BooleanField(default=False)

    def is_active(self):
        if self.has_expired:
            return False
        curr_date = timezone.now()
        diff = abs((curr_date - self.last_accessed).days)
        # 1 month expiration date
        if diff > 30:
            self.has_expired = True
            self.save()
            return False
        else:
            self.last_accessed = curr_date
            self.save()
            return True
