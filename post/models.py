from django.db import models
from location.models import Location
from django.contrib.auth.models import User


class Post (models.Model):
    location = models.ForeignKey(Location)
    comment = models.TextField()
    rating = models.IntegerField()
    is_free = models.BooleanField()
    user = models.ForeignKey(User, related_name="posts")
    is_anonymous = models.BooleanField()
    upvotes = models.ManyToManyField(User, related_name="upvoted_posts")
    downvotes = models.ManyToManyField(User, related_name="downvoted_posts")

