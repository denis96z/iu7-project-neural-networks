import api.models
from django.db import migrations, models
import django.db.models.deletion
import django_resized.forms
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ChineseCharacterImage',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('img_set_type', models.CharField(choices=[('tr', 'Тренировочная'), ('ts', 'Тестовая')], max_length=2, verbose_name='Выборка')),
                ('img_width', models.PositiveIntegerField(editable=False)),
                ('img_height', models.PositiveIntegerField(editable=False)),
                ('img', django_resized.forms.ResizedImageField(crop=None, force_format='PNG', keep_meta=True, quality=95, size=[50, 100], upload_to=api.models.image_path, verbose_name='Изображение')),
            ],
            options={
                'verbose_name': 'Изображение иероглифа',
                'verbose_name_plural': 'Изображения иероглифов',
                'ordering': ['img_set_type', 'img_class', 'id'],
            },
        ),
        migrations.CreateModel(
            name='ImageClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(choices=[('京', '京'), ('渝', '渝'), ('沪', '沪'), ('津', '津'), ('皖', '皖'), ('闽', '闽'), ('甘', '甘'), ('粤', '粤'), ('贵', '贵'), ('琼', '琼'), ('冀', '冀'), ('黑', '黑'), ('豫', '豫'), ('鄂', '鄂'), ('湘', '湘'), ('苏', '苏'), ('赣', '赣'), ('吉', '吉'), ('辽', '辽'), ('青', '青'), ('陕', '陕'), ('鲁', '鲁'), ('晋', '晋'), ('川', '川'), ('云', '云'), ('浙', '浙'), ('桂', '桂'), ('蒙', '蒙'), ('宁', '宁'), ('藏', '藏'), ('新', '新')], max_length=1, unique=True, verbose_name='Символ')),
            ],
            options={
                'verbose_name': 'Иероглифический символ',
                'verbose_name_plural': 'Иероглифические символы',
                'ordering': ['label'],
            },
        ),
        migrations.CreateModel(
            name='NeuralNetworkModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to=api.models.model_path, verbose_name='Файл')),
                ('version', models.CharField(max_length=5, unique=True, verbose_name='Версия')),
                ('img_width', models.PositiveIntegerField(editable=False)),
                ('img_height', models.PositiveIntegerField(editable=False)),
                ('img_classes', models.ManyToManyField(to='api.ImageClass')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
                'ordering': ['-version'],
            },
        ),
        migrations.AddField(
            model_name='chinesecharacterimage',
            name='img_class',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.ImageClass', verbose_name='Класс'),
        ),
    ]
