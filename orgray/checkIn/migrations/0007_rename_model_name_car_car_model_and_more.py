# Generated by Django 4.2.7 on 2023-11-10 22:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkIn', '0006_car'),
    ]

    operations = [
        migrations.RenameField(
            model_name='car',
            old_name='model_name',
            new_name='car_model',
        ),
        migrations.RenameField(
            model_name='car',
            old_name='available',
            new_name='is_available',
        ),
    ]
