# Generated by Django 4.2.1 on 2024-07-12 20:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0004_rename_сontracts_contracts_alter_clients_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clients',
            name='district_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='district_id', to='authapp.districts', verbose_name='регион'),
        ),
        migrations.AlterField(
            model_name='managers',
            name='branch_id',
            field=models.ManyToManyField(related_name='branch', to='authapp.branches', verbose_name='отрасль'),
        ),
        migrations.AlterField(
            model_name='managers',
            name='district_id',
            field=models.ManyToManyField(related_name='district', to='authapp.districts', verbose_name='федеральный округ'),
        ),
    ]
