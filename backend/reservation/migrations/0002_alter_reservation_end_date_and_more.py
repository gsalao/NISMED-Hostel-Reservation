# Generated by Django 5.2.2 on 2025-06-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reservation', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='end_date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='start_date',
            field=models.DateField(),
        ),
    ]
