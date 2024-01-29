from django.core.exceptions import ValidationError


def validate_video(value):
    ext = value.name.rsplit('.', 1)[1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'gif', 'mp4', 'ogg', 'webm']:
        raise ValidationError(
            'Video content must be in mp4, ogg and webm.')


def validate_image(value):
    ext = value.name.rsplit('.', 1)[1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'gif']:
        raise ValidationError(
            'Image content must be in jpg, jpeg, png, gif.')
