# Generated by Django 4.2.1 on 2024-06-07 16:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='clients',
            old_name='user',
            new_name='user_id',
        ),
        migrations.RenameField(
            model_name='managers',
            old_name='user',
            new_name='user_id',
        ),
    ]