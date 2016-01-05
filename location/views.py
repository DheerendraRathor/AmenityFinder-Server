from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_403_FORBIDDEN
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.http import HttpResponseForbidden

from post.serializers import PostSerializer
from core.pagination import DefaultCursorPagination
from core.mixins import SerializerClassRequestContextMixin
from .models import Location
from post.models import Post
from .serializers import LocationSerializer, BBoxSerializer, NewLocationSerializer, UpdateLocationSerializer


class LocationViewSet(SerializerClassRequestContextMixin, viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('rating')
    serializer_class = LocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def list(self, request, *args, **kwargs):
        return HttpResponseForbidden()

    @list_route(methods=['POST'], permission_classes=[])
    def search_by_bbox(self, request):
        """
        Get locations by BBox
        ---
        request_serializer: BBoxSerializer
        """

        serialized_data = BBoxSerializer(data=request.data)
        if serialized_data.is_valid():
            min_lat = serialized_data.validated_data['lat_min']
            max_lat = serialized_data.validated_data['lat_max']
            min_long = serialized_data.validated_data['long_min']
            max_long = serialized_data.validated_data['long_max']
            data = self.get_queryset().filter(latitude__range=[min_lat, max_lat], longitude__range=[min_long, max_long])
            locations = self.get_context_serializer_class(self.serializer_class, data, many=True)
            return Response({'results': locations.data})
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(permission_classes=[IsAuthenticated])
    def current_post(self, request, pk):
        """
        Get user's current location
        ---
        """
        location = get_object_or_404(Location, pk=pk)
        post = Post.objects.filter(user=request.user, location=location)
        if post.exists():
            data = post[0]
            post = self.get_context_serializer_class(PostSerializer, data)
            return Response({'success': True, 'result': post.data})
        else:
            return Response({'success': False, 'result': None})

    @detail_route(pagination_class=DefaultCursorPagination)
    def get_posts(self, request, pk):
        """
        Get paginated posts of a location id
        ---
        response_serializer: PostSerializer
        """
        loc = get_object_or_404(Location, pk=pk)
        loc_posts = loc.posts.all()
        posts = self.paginate_queryset(loc_posts)
        posts = self.get_context_serializer_class(PostSerializer, posts, many=True)
        return self.get_paginated_response(posts.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new location.
        ---
        request_serializer: NewLocationSerializer
        """
        serialized_data = NewLocationSerializer(data=request.data)
        if serialized_data.is_valid():
            lat_check = float('%.4f' % serialized_data.validated_data['latitude'])
            long_check = float('%.4f' % serialized_data.validated_data['longitude'])
            location = Location.objects.filter(latitude=lat_check, longitude=long_check)
            if location.exists():
                location = location[0]
            else:
                location = Location.objects.create(
                    latitude=serialized_data.validated_data['latitude'],
                    longitude=serialized_data.validated_data['longitude'],
                    name=serialized_data.validated_data['name'],
                    is_free=serialized_data.validated_data['is_free'],
                    male=serialized_data.validated_data['male'],
                    female=serialized_data.validated_data['female'],
                    is_anonymous=serialized_data.validated_data['is_anonymous'],
                    user=request.user,
                )

                location.save()

            return Response(self.serializer_class(location).data)
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(methods=['POST'])
    def flag_post(self, request, pk):
        """
        Remove vote if present.
        ---
        parameters_strategy:
            form: replace
        """
        location = self.get_object()
        location.flags.add(request.user)
        return Response(self.get_context_serializer_class(LocationSerializer, location).data)

    def update(self, request, *args, **kwargs):
        """
        Update the location; can update lat, long, name, is_free, male, female, is_anonymous
        ---
        request_serializer: location.serializers.UpdateLocationSerializer
        response_serializer: location.serializers.LocationSerializer
        """
        serialized_data = UpdateLocationSerializer(data=request.data)
        location = self.get_object()

        if location.user != request.user:
            return Response({'success': False, 'message': 'Unauthorized access'}, status=HTTP_403_FORBIDDEN)
        else:
            if serialized_data.is_valid():
                try:
                    location.latitude = serialized_data.validated_data['latitude']
                except KeyError:
                    pass

                try:
                    location.longitude = serialized_data.validated_data['longitude']
                except KeyError:
                    pass

                try:
                    location.name = serialized_data.validated_data['name']
                except KeyError:
                    pass

                try:
                    location.is_free = serialized_data.validated_data['is_free']
                except KeyError:
                    pass

                try:
                    location.male = serialized_data.validated_data['male']
                except KeyError:
                    pass

                try:
                    location.female = serialized_data.validated_data['female']
                except KeyError:
                    pass

                try:
                    location.is_anonymous = serialized_data.validated_data['is_anonymous']
                except KeyError:
                    pass

                location.save()
                return Response(self.get_context_serializer_class(LocationSerializer, location).data)
            else:
                return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)
