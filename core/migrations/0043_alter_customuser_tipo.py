# Generated by Django 5.2.1 on 2025-05-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0042_customuser_tipo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='tipo',
            field=models.CharField(choices=[('cliente', 'Cliente'), ('vendedor', 'Vendedor'), ('bodeguero', 'Bodeguero'), ('contador', 'Contador'), ('administrador', 'Administrador')], default='Cliente', max_length=20, verbose_name='Tipo'),
        ),
    ]
