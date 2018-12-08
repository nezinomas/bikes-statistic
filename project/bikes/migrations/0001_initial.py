# Generated by Django 2.0.7 on 2018-11-23 14:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('full_name', models.CharField(blank=True, max_length=150)),
                ('short_name', models.CharField(max_length=20, unique=True)),
                ('slug', models.SlugField(editable=False)),
            ],
            options={
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='BikeInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('component', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=254)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bike_info', to='bikes.Bike')),
            ],
        ),
        migrations.CreateModel(
            name='Component',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ComponentStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('price', models.FloatField(blank=True, null=True)),
                ('brand', models.TextField(blank=True)),
                ('bike', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bike', to='bikes.Bike')),
                ('component', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='component', to='bikes.Component')),
            ],
        ),
    ]
