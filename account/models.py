from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.validators import validate_image


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    follows = models.ManyToManyField('self', symmetrical=False, blank=True)


def create_profile_image_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'


def create_profile_cover_path(instance, filename):
    return f'profile_covers/{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=create_profile_image_path, default='no_pic.png', blank=True,
                                      validators=[validate_image])
    profile_cover = models.ImageField(upload_to=create_profile_cover_path, null=True, blank=True,
                                      validators=[validate_image])
