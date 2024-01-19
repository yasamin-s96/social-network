from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    email = models.EmailField()
    saved_posts = models.ManyToManyField('network.Post', related_name="saved_by")
    follows = models.ManyToManyField('self', symmetrical=False)


def create_profile_image_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'


def create_profile_cover_path(instance, filename):
    return f'profile_covers/{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=create_profile_image_path, default='no_pic.png', blank=True)
    profile_cover = models.ImageField(upload_to=create_profile_cover_path, null=True, blank=True)
