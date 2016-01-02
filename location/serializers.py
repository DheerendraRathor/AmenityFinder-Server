from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    flag_count = serializers.IntegerField(source='flags.count')

    class Meta:
        model = Location
        fields = ['id', 'latitude', 'longitude', 'name', 'is_free', 'rating', 'user', 'male', 'female', 'flag_count',
                  'created']


class BBoxSerializer(serializers.Serializer):
    lat_min = serializers.FloatField(min_value=-90.0, max_value=90.0)
    long_min = serializers.FloatField(min_value=-180.0, max_value=180.0)
    lat_max = serializers.FloatField(min_value=-90.0, max_value=90.0)
    long_max = serializers.FloatField(min_value=-180.0, max_value=180.0)

class NewLocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField(min_value=-90.0, max_value=90.0)
    longitude = serializers.FloatField(min_value=-180.0, max_value=180.0)
    name = serializers.CharField()
    is_free = serializers.BooleanField()
    male = serializers.BooleanField()
    female = serializers.BooleanField()
