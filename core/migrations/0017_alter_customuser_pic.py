# Generated by Django 5.0.6 on 2024-06-26 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_alter_customuser_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='pic',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics'),
        ),
    ]
