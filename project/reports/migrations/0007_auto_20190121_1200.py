# Generated by Django 2.1.4 on 2019-01-21 10:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0006_auto_20190108_1458'),
    ]

    operations = [
        migrations.AlterField(
            model_name='data',
            name='date',
            field=models.DateField(default=datetime.date(2019, 1, 21)),
        ),
    ]
