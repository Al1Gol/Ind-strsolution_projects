# Generated by Django 4.2.1 on 2024-07-12 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikiapp', '0005_alter_files_file_alter_images_img_alter_sections_img_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='wiki_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='wiki_id', to='wikiapp.wiki', verbose_name='id wiki'),
        ),
    ]