# Generated by Django 5.0.7 on 2024-08-01 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_clients_district_id_alter_managers_branch_id_and_more'),
        ('projectsapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projects',
            name='contract_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='authapp.contracts', verbose_name='договор'),
        ),
    ]