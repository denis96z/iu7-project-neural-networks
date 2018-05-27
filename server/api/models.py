import os
import uuid

from django.db import models
from django_resized import ResizedImageField

IMG_SET_TYPES = (
    ('tr', 'train'),
    ('ts', 'test'),
)

IMG_SET_TYPE_LEN = len(IMG_SET_TYPES[0][0])


def image_filename(instance, _):
    return os.path.join('sets', instance.img_set_type, instance.img_class, '{0}.png'.format(instance.id))


class ChineseCharacterImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img_class = models.CharField(max_length=1)
    img_set_type = models.CharField(max_length=IMG_SET_TYPE_LEN, choices=IMG_SET_TYPES)
    img = ResizedImageField(upload_to=image_filename, force_format='PNG')


def model_filename(instance, _):
    return os.path.join('models', '{0}.h5'.format(instance.version))


class NeuralNetworkModel(models.Model):
    file = models.FileField(upload_to=model_filename)
    version = models.CharField(max_length=5, unique=True)

    class Meta:
        ordering = ['-version']
