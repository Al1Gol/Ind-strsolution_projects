# Generated by Django 4.2.1 on 2024-07-23 15:49

from django.db import migrations, models
import wikiapp.validators


class Migration(migrations.Migration):

    dependencies = [
        ('wikiapp', '0007_wiki_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='img',
            field=models.FileField(blank=True, null=True, upload_to='wiki/icons/menu/', validators=[wikiapp.validators.validate_svg_extension], verbose_name='иконка'),
        ),
        migrations.AlterField(
            model_name='wiki',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='wiki/icons/logo/', validators=[wikiapp.validators.validate_svg_extension], verbose_name='иконка'),
        ),
    ]
