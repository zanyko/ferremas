# Generated by Django 5.2.1 on 2025-05-21 01:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0072_alter_informedesemp_fecha'),
    ]

    operations = [
        migrations.AddField(
            model_name='informedesemp',
            name='idUser',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='idUser'),
        ),
    ]
