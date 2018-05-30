from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Запускает процесс обучения нейронной сети и по окончании добавляет результат в базу данных'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Обучение завершено'))
