from django.db import models
from django.contrib.auth.models import User
from simple_history.models import HistoricalRecords


class Location (models.Model):
    latitude = models.FloatField(db_index=True)
    longitude = models.FloatField(db_index=True)
    name = models.CharField(max_length=64)
    is_free = models.BooleanField(default=True)
    rating = models.FloatField(default=0.0)
    user = models.ForeignKey(User)
    male = models.BooleanField(default=True)
    female = models.BooleanField(default=True)
    flags = models.ManyToManyField(User, related_name='flagged_locations', blank=True)
    _history_ = HistoricalRecords()

    def __str__(self):
        return self.name
