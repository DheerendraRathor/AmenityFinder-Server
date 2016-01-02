from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.decorators import list_route, detail_route
from rest_framework.pagination import CursorPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST

from post.serializers import PostSerializer
from .models import Location
from .serializers import LocationSerializer, BBoxSerializer, NewLocationSerializer


class DefaultCursorPagination(CursorPagination):
    page_size = 20


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all().order_by('rating')
    serializer_class = LocationSerializer

    @list_route(methods=['POST'])
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
            locations = self.serializer_class(data, many=True)
            return Response(locations.data)
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)

    @detail_route(pagination_class=DefaultCursorPagination)
    def get_posts(self, request, pk):
        loc = get_object_or_404(Location, pk=pk)
        loc_posts = loc.posts.all()
        posts = self.paginate_queryset(loc_posts)
        posts = PostSerializer(posts, many=True)
        return self.get_paginated_response(posts.data)

    def create(self, request, *args, **kwargs):
        """
        Creates a new location.
        ---
        request_serializer: NewLocationSerializer
        """
        serialized_data = NewLocationSerializer(data=request.data)
        if serialized_data.is_valid():

            location = Location.objects.create(
                latitude=serialized_data.validated_data['latitude'],
                longitude=serialized_data.validated_data['longitude'],
                name=serialized_data.validated_data['name'],
                is_free=serialized_data.validated_data['is_free'],
                male=serialized_data.validated_data['male'],
                female=serialized_data.validated_data['female'],
            )

            location.save()

            return Response(self.get_serializer_class(location))
        else:
            return Response(serialized_data.errors, status=HTTP_400_BAD_REQUEST)




