# Generated by Django 5.2.1 on 2025-05-21 23:06

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0078_alter_gasto_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='informemensual',
            name='idUser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='idUser'),
        ),
    ]
