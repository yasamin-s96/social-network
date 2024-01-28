from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify

from utils.validators import validate_image


# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    follows = models.ManyToManyField('self', symmetrical=False, related_name='followed_by', blank=True)

    def serialize(self):
        return {
            'display_name': f'{self.get_full_name()}'.title() if self.first_name else self.username.title(),
            'username': self.username,
            'profile_pic': self.profile.profile_image.url
        }


def create_profile_image_path(instance, filename):
    return f'profile_images/{instance.user.id}/{filename}'


def create_profile_cover_path(instance, filename):
    return f'profile_covers/{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to=create_profile_image_path, default='no_pic.png', blank=True,
                                      validators=[validate_image])
    profile_cover = models.ImageField(upload_to=create_profile_cover_path, default='no_cover.png', blank=True,
                                      validators=[validate_image])
