from rest_framework import viewsets
from .models import Amenity
from .serializers import AmenitySerializer


class AmenityViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Amenity.objects.all().order_by('id')
    serializer_class = AmenitySerializer
