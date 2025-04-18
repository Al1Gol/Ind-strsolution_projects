# Generated by Django 5.0.7 on 2025-03-10 19:49

import wikiapp.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wikiapp', '0010_alter_files_file_alter_videos_video'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiki',
            name='logo_admin',
            field=models.FileField(blank=True, null=True, upload_to='wiki/icons/admin_logo/', validators=[wikiapp.validators.validate_svg_extension], verbose_name='иконка в админке'),
        ),
    ]
