from rest_framework import serializers
from .models import Location
from amenity.serializers import AmenitySerializer


class LocationSerializer(serializers.ModelSerializer):
    amenity = AmenitySerializer()

    class Meta:
        model = Location
