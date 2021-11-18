# Generated by Django 3.2.5 on 2021-07-24 17:37

import ckeditor.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('content', ckeditor.fields.RichTextField()),
                ('type', models.CharField(choices=[('Scripts', 'Скрипты'), ('Configs', 'Конфиги'), ('Weather', 'Погода'), ('Textures', 'Текстуры'), ('Models', 'Моделирование')], max_length=50)),
                ('stalker', models.CharField(choices=[('CoP', 'Зов Припяти'), ('Cs', 'Чистое Небо'), ('SoC', 'Тень Чернобыля'), ('All', 'Все части')], max_length=50)),
                ('date_publish', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
