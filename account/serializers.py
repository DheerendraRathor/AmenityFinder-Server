from rest_framework import serializers

from account.models import UserProfile


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserProfile
