# Generated by Django 5.2.1 on 2025-05-21 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0074_informemensual_iduser_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='balancemensual',
            name='descripcion',
        ),
        migrations.AddField(
            model_name='balancemensual',
            name='gastos',
            field=models.IntegerField(blank=True, default=0, editable=False, null=True, verbose_name='Gastos'),
        ),
        migrations.AddField(
            model_name='balancemensual',
            name='notas',
            field=models.TextField(blank=True, null=True, verbose_name='Notas'),
        ),
        migrations.AlterField(
            model_name='balancemensual',
            name='fecha',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Fecha'),
        ),
    ]
