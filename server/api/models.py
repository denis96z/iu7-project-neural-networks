import os
import uuid

from django.db import models
from django_resized import ResizedImageField

IMG_CLASSES = (
    ('京', '京'), ('渝', '渝'), ('沪', '沪'), ('津', '津'), ('皖', '皖'),
    ('闽', '闽'), ('甘', '甘'), ('粤', '粤'), ('贵', '贵'), ('琼', '琼'),
    ('冀', '冀'), ('黑', '黑'), ('豫', '豫'), ('鄂', '鄂'), ('湘', '湘'),
    ('苏', '苏'), ('赣', '赣'), ('吉', '吉'), ('辽', '辽'), ('青', '青'),
    ('陕', '陕'), ('鲁', '鲁'), ('晋', '晋'), ('川', '川'), ('云', '云'),
    ('浙', '浙'), ('桂', '桂'), ('蒙', '蒙'), ('宁', '宁'), ('藏', '藏'),
    ('新', '新'),
)


class ImageClass(models.Model):
    label = models.CharField(max_length=1, unique=True,
                             choices=IMG_CLASSES, verbose_name='Символ')

    def __str__(self):
        return self.label

    class Meta:
        ordering = ['label']
        verbose_name = 'Иероглифический символ'
        verbose_name_plural = 'Иероглифические символы'


from api.settings import DJANGORESIZED_DEFAULT_FORCE_FORMAT

DJANGORESIZED_DEFAULT_FORCE_FORMAT_LOWER_CASE = \
    DJANGORESIZED_DEFAULT_FORCE_FORMAT.lower()

IMG_SET_TYPES = (
    ('tr', 'Тренировочная'),
    ('ts', 'Тестовая'),
)

IMG_SET_TYPE_LEN = len(IMG_SET_TYPES[0][0])


def image_filename(instance, _):
    return os.path.join(instance.img_set_type, instance.img_class.label,
                        '{0}.{1}'.format(instance.id, DJANGORESIZED_DEFAULT_FORCE_FORMAT_LOWER_CASE))


def image_path(instance, _):
    return os.path.join('sets', image_filename(instance, _))


class ChineseCharacterImage(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    img_class = models.ForeignKey(ImageClass, on_delete=models.CASCADE, verbose_name='Класс')
    img_set_type = models.CharField(max_length=IMG_SET_TYPE_LEN, choices=IMG_SET_TYPES, verbose_name='Выборка')
    img_width = models.PositiveIntegerField(editable=False)
    img_height = models.PositiveIntegerField(editable=False)
    img = ResizedImageField(upload_to=image_path, width_field='img_width',
                            height_field='img_height', verbose_name='Изображение')

    def __str__(self):
        return image_filename(self, None)

    class Meta:
        ordering = ['img_set_type', 'img_class', 'id']
        verbose_name = 'Изображение иероглифа'
        verbose_name_plural = 'Изображения иероглифов'


def model_path(instance, _):
    return os.path.join('models', '{0}.h5'.format(instance.version))


NEURAL_NETWORK_MODEL_VERSION_LEN = 5


class NeuralNetworkModel(models.Model):
    file = models.FileField(upload_to=model_path, verbose_name='Файл')
    version = models.CharField(max_length=NEURAL_NETWORK_MODEL_VERSION_LEN,
                               unique=True, verbose_name='Версия')
    img_width = models.PositiveIntegerField(editable=False)
    img_height = models.PositiveIntegerField(editable=False)
    img_classes = models.ManyToManyField(ImageClass)

    def __str__(self):
        return self.version

    class Meta:
        ordering = ['-version']
        verbose_name = 'Модель'
        verbose_name_plural = 'Модели'
