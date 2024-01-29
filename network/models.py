from django.db import models
from django.contrib.auth import get_user_model
from utils.validators import validate_video, validate_image

User = get_user_model()


# Create your models here.

class Post(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    text_content = models.CharField(max_length=256, blank=True)
    image_content = models.ImageField(upload_to='posts/%Y/%m/%d', blank=True, validators=[validate_image])
    video_content = models.FileField(upload_to='posts/%Y/%m/%d', blank=True, validators=[validate_video])
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    saved_by = models.ManyToManyField(User, related_name="saved_posts", blank=True)
    posted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=('-posted_at',), name='post_created_at_idx')
        ]
        ordering = ['-posted_at']

    def __str__(self):
        return self.text_content


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='post_comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    content = models.CharField(max_length=256)
    commented_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=('-commented_at',), name='commented_at_idx')
        ]
        ordering = ['-commented_at']

    def serialize(self):
        return {
            'id': self.pk,
            'user': self.user.serialize(),
            'content': self.content,
            'commented_at': self.commented_at.strftime('%I:%M %p %d %Y')
        }
