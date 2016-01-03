from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()
