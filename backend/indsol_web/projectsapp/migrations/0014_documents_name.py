# Generated by Django 5.0.7 on 2024-09-03 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projectsapp', '0013_documents'),
    ]

    operations = [
        migrations.AddField(
            model_name='documents',
            name='name',
            field=models.CharField(default=1, max_length=1000, verbose_name='Наименование файла'),
            preserve_default=False,
        ),
    ]
