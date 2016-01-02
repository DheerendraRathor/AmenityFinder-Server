from rest_framework import serializers

from core.serializers import UserSerializer
from .models import Post


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
    location = serializers.IntegerField()
    comment = serializers.CharField()
    rating = serializers.FloatField(min_value=0.0, max_value=5.0)
    is_anonymous = serializers.BooleanField()


