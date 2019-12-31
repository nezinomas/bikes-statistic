# Generated by Django 3.0.1 on 2019-12-31 12:21

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bikes', '0002_auto_20191230_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='components', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='component',
            name='name',
            field=models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator(99), django.core.validators.MinLengthValidator(3)]),
        ),
        migrations.AlterUniqueTogether(
            name='component',
            unique_together={('user', 'name')},
        ),
    ]
