# Generated by Django 5.2.2 on 2025-06-20 06:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('guest', '0001_initial'),
        ('room', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('CHECKED IN', 'CHECKED IN'), ('NO SHOW', 'NO SHOW'), ('CANCELLED', 'CANCELLED'), ('CHECKED OUT', 'CHECKED OUT')], default='CHECKED IN', max_length=1024)),
                ('reservation_date', models.DateTimeField(auto_now_add=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
                ('for_person_name', models.CharField(max_length=1024)),
                ('by_person_name', models.CharField(max_length=1024)),
                ('male_count', models.IntegerField()),
                ('female_count', models.IntegerField()),
                ('remarks', models.TextField(blank=True, null=True)),
                ('single_a_room_count', models.IntegerField(default=0)),
                ('double_a_room_count', models.IntegerField(default=0)),
                ('single_b_room_count', models.IntegerField(default=0)),
                ('double_b_room_count', models.IntegerField(default=0)),
                ('single_c_room_count', models.IntegerField(default=0)),
                ('double_c_room_count', models.IntegerField(default=0)),
                ('triple_c_room_count', models.IntegerField(default=0)),
                ('guest_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='guest.guest')),
            ],
        ),
        migrations.CreateModel(
            name='ReservedRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reservation.reservation')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.room')),
                ('room_rate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='room.roomrate')),
            ],
        ),
    ]
