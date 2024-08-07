# Generated by Django 5.0.7 on 2024-08-05 03:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0008_delete_contracts'),
        ('projectsapp', '0009_remove_projects_contract_id_delete_contracts'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contracts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contract_number', models.CharField(max_length=50, verbose_name='номер договора')),
                ('client_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.clients', verbose_name='клиент')),
            ],
            options={
                'verbose_name': 'Договоры',
                'verbose_name_plural': 'Договоры',
            },
        ),
        migrations.AddField(
            model_name='projects',
            name='contract_id',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tags', to='projectsapp.contracts', verbose_name='договор'),
            preserve_default=False,
        ),
    ]
