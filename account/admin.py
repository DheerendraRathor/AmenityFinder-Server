from django.contrib import admin
from .models import UserProfile, UserToken


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'picture', 'plus_points', 'minus_points', 'user_level', 'is_banned']


@admin.register(UserToken)
class UserTokenAdmin(admin.ModelAdmin):
    list_display = ['user', 'token']

