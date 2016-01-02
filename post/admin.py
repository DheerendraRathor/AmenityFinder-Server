from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id', 'location', 'comment', 'rating', 'user', 'is_anonymous', 'created']
