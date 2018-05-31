import os

from django.core.files import File
from django.core.management import BaseCommand

from keras import Sequential
from keras.layers import Conv2D, MaxPooling2D, Activation, Dense, Flatten, Dropout
from keras.optimizers import SGD
from keras.preprocessing.image import ImageDataGenerator

from api.models import ImageClass, NeuralNetworkModel, model_path
from api.settings import DJANGORESIZED_DEFAULT_SIZE, IMG_SET_TYPES


class Command(BaseCommand):
    help = 'Запускает процесс обучения нейронной сети и по окончании добавляет результат в базу данных'

    def add_arguments(self, parser):
        parser.add_argument('src_path', type=str)
        parser.add_argument('version', type=str)

    def handle(self, *args, **options):
        version = options['version']
        if len(version) > 5:
            self.stdout.write(self.style.ERROR('Код версии должен содержать не более 5 символов'))
            return
        if NeuralNetworkModel.objects.filter(version=version).exists():
            self.stdout.write(self.style.ERROR('Версия с указанным кодом уже существует'))
            return

        num_classes = ImageClass.objects.count()
        if num_classes == 0:
            self.stdout.write(self.style.ERROR('Отсутствуют классы изображений'))
            return

        img_width = DJANGORESIZED_DEFAULT_SIZE[0]
        img_height = DJANGORESIZED_DEFAULT_SIZE[1]
        classes = list(ImageClass.objects.all())

        model = Sequential()
        model.add(Conv2D(filters=64, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', data_format='channels_first',
                         input_shape=(1, img_width, img_height)))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='valid',
                               data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Conv2D(filters=128, kernel_size=(3, 3), strides=(1, 1),
                         padding='same', data_format='channels_first'))
        model.add(MaxPooling2D(pool_size=(2, 2), padding='valid',
                               data_format='channels_first'))
        model.add(Activation('relu'))
        model.add(Conv2D(filters=32, kernel_size=(2, 2), strides=(1, 1),
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

        tr_data_gen = ImageDataGenerator(
            rescale=1. / 255,
            shear_range=0.2,
            zoom_range=0.2,
            horizontal_flip=True,
            data_format='channels_first')
        train_generator = tr_data_gen.flow_from_directory(
            os.path.join(options['src_path'], IMG_SET_TYPES[0][0]),
            target_size=(img_width, img_height),
            color_mode='grayscale',
            batch_size=16,
            class_mode='binary')

        self.stdout.write(self.style.SUCCESS('Данные для обучения сформированы'))

        ts_data_gen = ImageDataGenerator(
            rescale=1. / 255,
            data_format='channels_first')
        test_generator = ts_data_gen.flow_from_directory(
            os.path.join(options['src_path'], IMG_SET_TYPES[1][0]),
            target_size=(img_width, img_height),
            color_mode='grayscale',
            batch_size=16,
            class_mode='binary')

        self.stdout.write(self.style.SUCCESS('Данные для тестирования сформированы'))

        # model.fit_generator(
        #     train_generator,
        #     steps_per_epoch=2000,
        #     epochs=50,
        #     validation_data=test_generator,
        #     validation_steps=800)

        self.stdout.write(self.style.SUCCESS('Обучение завершено'))

        temp_filename = 'temp.h5'
        model.save(temp_filename)
        file = File(open(temp_filename, 'rb'))

        nn_model = NeuralNetworkModel()
        nn_model.version = version
        nn_model.img_width = img_width
        nn_model.img_height = img_height
        nn_model.file.save(model_path(nn_model, None), file, save=True)
        nn_model.save()
        nn_model.img_classes.add(*classes)
        nn_model.save()

        self.stdout.write(self.style.SUCCESS('Модель сохранена'))
