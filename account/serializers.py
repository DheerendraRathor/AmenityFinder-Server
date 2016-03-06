from rest_framework import serializers

from account.models import UserProfile
from location.models import Location
from post.models import Post, Picture
from core.serializers import UserSerializer

class LoginSerializer(serializers.Serializer):
    access_token = serializers.CharField()


class UserProfileSerializer(serializers.ModelSerializer):
    locations = serializers.SerializerMethodField()
    posts = serializers.SerializerMethodField()
    photos = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()

    def get_user(self, user_profile: UserProfile):
        return UserSerializer(user_profile.user).data

    def get_locations(self, user_profile: UserProfile):
        return Location.objects.all().filter(user=user_profile.user).count()

    def get_posts(self, user_profile: UserProfile):
        return Post.objects.all().filter(user=user_profile.user).count()

    def get_photos(self, user_profile: UserProfile):
        return Picture.objects.all().filter(user=user_profile.user).count()

    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'plus_points', 'minus_points', 'user_level', 'is_banned', 'locations',
                  'posts', 'photos']
