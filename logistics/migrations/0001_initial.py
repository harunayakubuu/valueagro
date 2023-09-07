# Generated by Django 3.2.16 on 2023-09-07 16:36

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
                'db_table': '',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Driver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128, region=None, verbose_name='Phone number')),
                ('date_of_birth', models.DateField()),
                ('driver_license', models.FileField(upload_to='')),
                ('picture', models.ImageField(upload_to='Pictures/Drivers')),
                ('status', models.CharField(choices=[('Active', 'Active'), ('Suspended', 'Suspended'), ('Disengaged', 'Disengaged')], default='Active', max_length=20)),
            ],
            options={
                'verbose_name': 'Driver',
                'verbose_name_plural': 'Drivers',
            },
        ),
        migrations.CreateModel(
            name='Vehicle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vehicle_number', models.CharField(max_length=10, unique=True)),
                ('chasis_number', models.CharField(max_length=30, unique=True)),
                ('picture', models.ImageField(upload_to='Pictures/Vehicle')),
                ('status', models.CharField(choices=[('AR', 'Active and Ready'), ('AB', 'Active and Busy'), ('BD', 'Broken Down'), ('UM', 'Undergoing Repairs'), ('UR', 'Undergoing Maintenance')], default='Active', max_length=20)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='logistics.category')),
                ('driver', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='logistics.driver')),
            ],
            options={
                'verbose_name': 'Vehicle',
                'verbose_name_plural': 'Vehicles',
            },
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('delivery_id', models.CharField(max_length=20)),
                ('delivery_address', models.CharField(max_length=100)),
                ('pickup_date', models.DateField()),
                ('expected_delivery_date', models.DateField()),
                ('transportation_charges', models.DecimalField(decimal_places=2, max_digits=10)),
                ('delivary_status', models.CharField(max_length=15)),
                ('verhicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='logistics.vehicle')),
            ],
            options={
                'verbose_name': 'Delivery',
                'verbose_name_plural': 'Deliveries',
            },
        ),
    ]
