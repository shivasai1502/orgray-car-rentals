# Generated by Django 4.2.7 on 2023-11-10 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkIn', '0003_rename_drivers_license_customer_drivers_license_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='reference_number',
        ),
    ]