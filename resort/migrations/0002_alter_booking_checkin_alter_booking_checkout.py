# Generated by Django 4.1.3 on 2023-03-27 09:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resort', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='checkin',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 27, 12, 12, 47, 294435)),
        ),
        migrations.AlterField(
            model_name='booking',
            name='checkout',
            field=models.DateTimeField(default=datetime.datetime(2023, 3, 27, 12, 12, 47, 294435)),
        ),
    ]
