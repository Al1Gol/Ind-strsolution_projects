# Generated by Django 5.0.7 on 2024-08-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0005_alter_clients_district_id_alter_managers_branch_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contracts',
            name='id',
        ),
        migrations.AlterField(
            model_name='contracts',
            name='contract_number',
            field=models.CharField(max_length=50, primary_key=True, serialize=False, verbose_name='номер договора'),
        ),
    ]
