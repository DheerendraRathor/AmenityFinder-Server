from django.contrib import admin

from .models import Post, Picture


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'comment', 'rating', 'user', 'is_anonymous', 'created']


@admin.register(Picture)
class Picture(admin.ModelAdmin):
    list_display = ['id', 'location', 'photo', 'user', 'is_anonymous', 'created']
