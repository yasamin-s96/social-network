from django.contrib import admin
from .models import Post, Comment


# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['creator', 'text_content', 'image_content', 'video_content']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'content', 'post', 'commented_at']
