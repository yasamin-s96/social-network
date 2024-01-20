from django.core.exceptions import ValidationError


def validate_image(value):
    ext = value.name.rsplit('.', 1)[1].lower()
    if ext not in ['jpg', 'png', 'jpeg', 'gif']:
        raise ValidationError('Image format must be jpg, jpeg, png or gif')


