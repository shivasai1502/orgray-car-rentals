# Generated by Django 4.2.7 on 2023-11-10 21:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkIn', '0004_remove_customer_reference_number'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='drivers_license_number',
            new_name='drivers_license',
        ),
    ]
