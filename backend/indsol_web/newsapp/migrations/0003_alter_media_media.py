# Generated by Django 4.2.1 on 2024-04-19 13:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsapp', '0002_rename_medianews_media'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='media',
            field=models.FileField(upload_to='news/media', verbose_name='файлы'),
        ),
    ]
