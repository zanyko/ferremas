# Generated by Django 5.0.6 on 2024-06-26 00:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_customuser_pic'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
