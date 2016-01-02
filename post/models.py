from django.db import models
from location.models import Location
from django.contrib.auth.models import User


class Post(models.Model):
    location = models.ForeignKey(Location, related_name='posts')
    comment = models.TextField()
    rating = models.IntegerField()
    user = models.ForeignKey(User, related_name='posts')
    is_anonymous = models.BooleanField()
    upvotes = models.ManyToManyField(User, related_name='upvoted_posts')
    downvotes = models.ManyToManyField(User, related_name='downvoted_posts')
    created = models.DateTimeField(auto_now_add=True)

