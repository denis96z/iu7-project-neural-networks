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
    img_class = models.CharField(max_length=1, blank=False, verbose_name='Класс изображения')
    img_set_type = models.CharField(max_length=IMG_SET_TYPE_LEN, blank=False,
                                    choices=IMG_SET_TYPES, verbose_name='Выборка')
    img = ResizedImageField(upload_to=image_filename, force_format='PNG', verbose_name='Изображение')

    def __str__(self):
        return image_filename(self, None)

    class Meta:
        verbose_name = 'Изображение иероглифа'
        verbose_name_plural = 'Изображения иероглифов'


def model_filename(instance, _):
    return os.path.join('models', '{0}.h5'.format(instance.version))


class NeuralNetworkModel(models.Model):
    file = models.FileField(upload_to=model_filename, verbose_name='Файл')
    version = models.CharField(max_length=5, unique=True, verbose_name='Версия')

    def __str__(self):
        return self.version

    class Meta:
        ordering = ['-version']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
