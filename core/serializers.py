from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    picture = serializers.URLField(source='profile.picture')
    # plus_points = serializers.IntegerField(source='profile.plus_points')
    # minus_points = serializers.IntegerField(source='profile.minus_points')
    # user_level = serializers.IntegerField(source='profile.user_level')
    # is_banned = serializers.BooleanField(source='profile.is_banned')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'picture']
