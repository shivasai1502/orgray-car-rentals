# Generated by Django 4.2.7 on 2023-11-09 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateField()),
                ('mobile_number', models.CharField(max_length=15)),
                ('address', models.TextField()),
                ('drivers_license', models.CharField(max_length=20)),
                ('id_type', models.CharField(choices=[('passport', 'Passport'), ('ssn', 'SSN'), ('state_id', 'State ID')], max_length=10)),
                ('id_number', models.CharField(max_length=20)),
                ('selected_car', models.CharField(choices=[('car1', 'Car 1'), ('car2', 'Car 2')], max_length=10)),
                ('reference_number', models.CharField(max_length=5, unique=True)),
            ],
        ),
    ]