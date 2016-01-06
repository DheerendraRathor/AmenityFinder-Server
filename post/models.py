from django.contrib.auth.models import User
from django.db import models

from location.models import Location


class Post(models.Model):
    location = models.ForeignKey(Location, related_name='posts')
    comment = models.TextField()
    rating = models.FloatField()
    user = models.ForeignKey(User, related_name='posts')
    is_anonymous = models.BooleanField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts', blank=True)
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts', blank=True)
    created = models.DateTimeField(auto_now_add=True)


class Picture(models.Model):
    location = models.ForeignKey(Location, related_name='picture')
    user = models.ForeignKey(User, related_name='picture')
    is_anonymous = models.BooleanField()
    photo = models.ImageField()
    flags = models.ManyToManyField(User, related_name='flagged_pictures', blank=True)
    created = models.DateTimeField(auto_now_add=True)
