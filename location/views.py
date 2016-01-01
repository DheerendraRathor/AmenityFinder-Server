from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer


class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Location.objects.all().order_by('id')
    serializer_class = LocationSerializer
