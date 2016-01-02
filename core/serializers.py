from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    picture = serializers.ImageField(source='profile.picture')

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'picture']
