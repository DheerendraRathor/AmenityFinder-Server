from django.contrib import admin
from .models import Location


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['id', 'latitude', 'longitude', 'name', 'is_free', 'rating', 'user', 'male', 'female', 'created']
