# Generated by Django 4.2.1 on 2024-04-08 15:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wikiapp', '0002_wiki'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='wiki',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='wiki', to='wikiapp.wiki', verbose_name='id wiki'),
            preserve_default=False,
        ),
    ]
