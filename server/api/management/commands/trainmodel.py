from django.core.management import BaseCommand

from keras import Model
from keras.applications import InceptionV3
from keras.layers import GlobalAveragePooling2D, Dense


def create_model(input_shape, num_classes):
    base_model = InceptionV3(weights='imagenet', include_top=False)
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    output = Dense(num_classes, activation='softmax')(x)
    model = Model(input=base_model.input, output=output)
    return model


class Command(BaseCommand):
    help = 'Запускает процесс обучения нейронной сети и по окончании добавляет результат в базу данных'

    def handle(self, *args, **options):
        create_model((65, 40), 33)
        self.stdout.write(self.style.SUCCESS('Обучение завершено'))
