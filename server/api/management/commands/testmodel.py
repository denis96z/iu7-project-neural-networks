from django.core.management import BaseCommand
from keras.models import load_model
from keras.preprocessing.image import ImageDataGenerator

from api.settings import DJANGORESIZED_DEFAULT_SIZE


class Command(BaseCommand):
    help = 'Запускает проверку модели на точность'

    def add_arguments(self, parser):
        parser.add_argument('model_path', type=str)
        parser.add_argument('test_path', type=str)

    def handle(self, *args, **options):
        model = load_model(options['model_path'])
        self.stdout.write(self.style.SUCCESS('Модель загружена'))
        model.summary()

        img_width = DJANGORESIZED_DEFAULT_SIZE[0]
        img_height = DJANGORESIZED_DEFAULT_SIZE[1]
        eval_data_gen = ImageDataGenerator(
            rescale=1. / 255)
        eval_generator = eval_data_gen.flow_from_directory(
            options['test_path'],
            target_size=(img_width, img_height),
            color_mode='grayscale',
            batch_size=16,
            class_mode='categorical')
        self.stdout.write(self.style.SUCCESS('Данные для тестирования загружены'))
        print(eval_generator.class_indices)

        score = model.evaluate_generator(eval_generator)
        self.stdout.write(self.style.SUCCESS('Тестирование завершено'))
        self.stdout.write('Точность: {0}'.format(score[1]))
