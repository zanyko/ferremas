# Generated by Django 5.2.1 on 2025-05-16 03:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_remove_customuser_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='preview',
            name='idDireccion',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.direccion', verbose_name='idDireccion'),
        ),
    ]
