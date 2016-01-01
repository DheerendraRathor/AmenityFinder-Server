from django.db import models
from amenity.models import Amenity
from django.contrib.auth.models import User


class Location (models.Model):
    lat_coord = models.FloatField()
    long_coord = models.FloatField()
    amenity = models.ForeignKey(Amenity)
    name = models.CharField(max_length=64)
    is_free = models.BooleanField()
    rating = models.FloatField(default=0.0)
    user = models.ForeignKey(User)