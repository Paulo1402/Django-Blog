from django.core.exceptions import ValidationError
from django.db.models.fields.files import ImageFieldFile


def validate_png(image: ImageFieldFile):
    if not image.name.lower().endswith('.png'):
        raise ValidationError('Imagem precisa ser PNG.')
