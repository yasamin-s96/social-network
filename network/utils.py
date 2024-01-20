from django.contrib import messages
from django.core.exceptions import ValidationError

from .models import Post


def manage_post_creation(user, text, picture):
    new_post = Post(creator=user)

    if text:
        new_post.text_content = text

    if picture:
        new_post.image_content = picture

    new_post.full_clean()
    new_post.save()


def manage_exception_object(request, e):
    """
    :param request: Request
    :param e: Exception
    :return: None
    """
    for error_list in e.error_dict.values():
        for error in error_list:
            if isinstance(error, ValidationError):
                messages.error(request, f'{error.message}')
            else:
                messages.error(request, f'{error}')
