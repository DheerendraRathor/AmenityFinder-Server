from django.http import HttpResponseForbidden
from rest_framework import viewsets
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN

from core.mixins import SerializerClassRequestContextMixin
from .models import Post
from .serializers import PostSerializer, NewPostSerializer, UpdatePostSerializer


class PostViewSet(SerializerClassRequestContextMixin, viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        """
        Create New Post and update ratings for that location
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

            this_location = post.location
            new_rating = this_location.rating * this_location.rating_count + serialized_data.validated_data['rating']
            new_rating /= (this_location.rating_count + 1)
            this_location.rating_count += 1
            this_location.rating = new_rating

            this_location.save()

            return Response(self.serializer_class(post))
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'])
    def upvote(self, request, pk):
        """
        Upvote a post and remove downvote of the user if present.
        ---
        parameters_strategy:
            form: replace
        """
        post = self.get_object()
        post.downvotes.remove(request.user)
        post.upvotes.add(request.user)
        return Response(self.get_context_serializer_class(PostSerializer, post).data)

    @detail_route(methods=['POST'])
    def downvote(self, request, pk):
        """
        Downvote a post and remove upvote of the user if present.
        ---
        parameters_strategy:
            form: replace
        """
        post = self.get_object()
        post.upvotes.remove(request.user)
        post.downvotes.add(request.user)
        return Response(self.get_context_serializer_class(PostSerializer, post).data)

    def destroy(self, request, *args, **kwargs):
        """
        Remove post.
        ---
        parameters_strategy:
            form: replace
        """
        post = self.get_object()
        if request.user is post.user:
            post.delete()
            return Response({'status': 'Delete Successful'})
        else:
            return HttpResponseForbidden()

    def update(self, request, *args, **kwargs):
        """
        Update existing post; Only comment, rating and is_anonymous can be updated.
        ---
        request_serializer: post.serializers.UpdatePostSerializer
        response_serializer: post.serializers.PostSerializer
        """
        serialized_data = UpdatePostSerializer(data=request.data)
        post = self.get_object()
        if post.user != request.user:
            return Response({'success': False, 'message': 'Unauthorized access'}, status=HTTP_403_FORBIDDEN)
        else:
            if serialized_data.is_valid():
                try:
                    post.comment = serialized_data.validated_data['comment']
                except KeyError:
                    pass

                try:
                    post.rating = serialized_data.validated_data['rating']
                except KeyError:
                    pass

                try:
                    post.is_anonymous = serialized_data.validated_data['is_anonymous']
                except KeyError:
                    pass

                post.save()
                return Response(self.get_context_serializer_class(PostSerializer, post).data)
            else:
                return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)
