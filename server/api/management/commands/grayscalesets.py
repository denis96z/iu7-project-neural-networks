import os

from PIL import Image
from django.core.management import BaseCommand


def list_all_files(src_path, dest_path, short_path):
    files = []
    os.mkdir(dest_path)
    for f in os.listdir(src_path):
        if os.path.isdir(os.path.join(src_path, f)):
            files += list_all_files(os.path.join(src_path, f),
                                    os.path.join(dest_path, f),
                                    os.path.join(short_path, f))
        else:
            files.append(os.path.join(short_path, f))
    return files


class Command(BaseCommand):
    help = 'Переводит цветные изображения в изображения в градациях серого цвета'

    def add_arguments(self, parser):
        parser.add_argument('src_path', type=str)
        parser.add_argument('dest_path', type=str)

    def handle(self, *args, **options):
        if not os.path.exists(options['src_path']):
            self.stdout.write(self.style.ERROR('Не удалось прочитать из указанной директории: не существует'))
            return
        if os.path.exists(options['dest_path']):
            self.stdout.write(self.style.ERROR('Невозможно создать указанную директорию: уже существует'))
            return

        src_paths = list_all_files(options['src_path'], options['dest_path'], '')
        for path in src_paths:
            src = os.path.join(options['src_path'], path)
            img = Image.open(src).convert('LA')
            dest = os.path.join(options['dest_path'], path)
            img.save(dest)

        self.stdout.write(self.style.SUCCESS('Изображение успешно преобразованы в градации серого цвета'))
