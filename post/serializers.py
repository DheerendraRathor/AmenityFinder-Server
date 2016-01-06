import base64
import binascii
import uuid

import django.utils.six
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from rest_framework import serializers

from core.serializers import UserSerializer
from location.models import Location
from .models import Post, Picture


class PostSerializer(serializers.ModelSerializer):
    upvotes = serializers.IntegerField(source='upvotes.count')
    downvotes = serializers.IntegerField(source='downvotes.count')
    user = serializers.SerializerMethodField()

    def get_user(self, post):
        try:
            user = self.context['request'].user
        except KeyError:
            user = None
        if user == post.user or not post.is_anonymous:
            return UserSerializer(post.user).data
        return None

    class Meta:
        model = Post
        fields = ['id', 'location', 'comment', 'rating', 'user', 'is_anonymous', 'upvotes', 'downvotes', 'created']


class NewPostSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    comment = serializers.CharField()
    rating = serializers.FloatField(min_value=0.0, max_value=5.0)
    is_anonymous = serializers.BooleanField()


class UpdatePostSerializer(serializers.Serializer):
    comment = serializers.CharField(required=False)
    rating = serializers.FloatField(min_value=0.0, max_value=5.0, required=False)
    is_anonymous = serializers.BooleanField(required=False)


class PictureSerializer(serializers.ModelSerializer):
    flags = serializers.IntegerField(source='flags.count')
    user = serializers.SerializerMethodField()

    def get_user(self, picture):
        try:
            user = self.context['request'].user
        except KeyError:
            user = None
        if user == picture.user or not picture.is_anonymous:
            return UserSerializer(picture.user).data
        return None

    class Meta:
        model = Picture
        fields = ['id', 'location', 'photo', 'user', 'is_anonymous', 'flags', 'created']


class Base64ImageField(serializers.ImageField):
    def to_internal_value(self, data):
        if isinstance(data, django.utils.six.string_types):
            try:
                decoded_data = base64.b64decode(data)
            except (TypeError, binascii.Error):
                raise ValidationError(_("Please upload a valid file"))

            name = uuid.uuid4()
            data = ContentFile(decoded_data, name=name.urn[9:] + '.jpg')
        return super(Base64ImageField, self).to_internal_value(data)


class NewPictureSerializer(serializers.Serializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())
    photo = Base64ImageField()
    is_anonymous = serializers.BooleanField()

