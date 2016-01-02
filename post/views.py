from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from .models import Post
from .serializers import PostSerializer, NewPostSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    # TODO: Add authentication
    def create(self, request, *args, **kwargs):
        """
        Create New Post
        ---
        request_serializer: NewPostSerializer
        """
        serialized_data = NewPostSerializer(data=request.data)
        if serialized_data.is_valid():

            post = Post.objects.create(
                    location=serialized_data.validated_data['location'],
                    comment=serialized_data.validated_data['comment'],
                    rating=serialized_data.validated_data['rating'],
                    is_anonymous=serialized_data.validated_data['is_anonymous'],
                    user=request.user,
            )

            post.save()

            return Response(self.serializer_class(post))
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)
