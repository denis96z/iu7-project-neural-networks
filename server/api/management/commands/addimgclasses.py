from django.core.management import BaseCommand

from api.models import ImageClass, IMG_CLASSES


class Command(BaseCommand):
    help = 'Добавляет в базу данных классы изображений иероглифов'

    def handle(self, *args, **options):
        ImageClass.objects.all().delete()
        for x in IMG_CLASSES:
            img_class = ImageClass()
            img_class.label = x[0]
            img_class.save()
        self.stdout.write(self.style.SUCCESS('Классы изображений иероглифов успешно добавлены'))
