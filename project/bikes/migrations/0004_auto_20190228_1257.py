# Generated by Django 2.1.7 on 2019-02-28 10:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bikes', '0003_auto_20190121_1200'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bikeinfo',
            options={'ordering': ['component']},
        ),
        migrations.AlterModelOptions(
            name='component',
            options={'ordering': ['name']},
        ),
    ]
