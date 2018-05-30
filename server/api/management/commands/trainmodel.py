from django.core.management import BaseCommand

from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten, Dropout
from keras.optimizers import SGD

from api.models import ImageClass
from api.settings import DJANGORESIZED_DEFAULT_SIZE


class Command(BaseCommand):
    help = 'Запускает процесс обучения нейронной сети и по окончании добавляет результат в базу данных'

    def handle(self, *args, **options):
        num_classes = ImageClass.objects.count()
        if num_classes == 0:
            self.stdout.write(self.style.ERROR('Отсутствуют классы изображений'))
            return

        img_width = DJANGORESIZED_DEFAULT_SIZE[0]
        img_height = DJANGORESIZED_DEFAULT_SIZE[1]

        model = Sequential()
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', data_format='channels_first',
                         input_shape=(1, img_width, img_height)))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='valid',
                               data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Conv2D(filters=216, kernel_size=(4, 4), strides=(1, 1),
                         padding='same', data_format='channels_first'))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='valid',
                               data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Conv2D(filters=16, kernel_size=(2, 2), strides=(1, 1),
                         padding='same', data_format='channels_first'))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='valid',
                               data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Flatten())
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.2))
        model.add(Dense(512, activation='relu'))
        model.add(Dropout(0.3))
        model.add(Dense(256, activation='relu'))
        model.add(Dropout(0.1))
        model.add(Dense(num_classes, activation='sigmoid'))
        model.compile(optimizer=SGD(lr=0.05), loss='categorical_crossentropy', metrics=['accuracy'])

        self.stdout.write(self.style.SUCCESS('Модель построена'))
        model.summary()

        self.stdout.write(self.style.SUCCESS('Обучение завершено'))
