# Generated by Django 5.2.2 on 2025-06-30 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0007_rename_guest_id_reservation_guest'),
    ]

    operations = [
        migrations.AddField(
            model_name='reservedroom',
            name='room_type_and_occupancy',
            field=models.CharField(blank=True, choices=[('A single', 'A single'), ('A double', 'A double'), ('B single', 'B single'), ('B double', 'B double'), ('C single', 'C single'), ('C double', 'C double'), ('C triple', 'C triple')], max_length=1024),
        ),
    ]
