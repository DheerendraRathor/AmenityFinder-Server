from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'lat_coord', 'long_coord', 'amenity', 'name', 'is_free', 'rating', 'user']

