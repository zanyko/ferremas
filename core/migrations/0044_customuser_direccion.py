# Generated by Django 5.2.1 on 2025-05-13 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_alter_customuser_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='direccion',
            field=models.CharField(default='sin direccion', max_length=255, verbose_name='Dirección'),
        ),
    ]
