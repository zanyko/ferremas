# Generated by Django 5.2.1 on 2025-05-13 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_customuser_direccion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='direccion',
        ),
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(default='sin direccion', max_length=255, verbose_name='Direccion'),
        ),
    ]
