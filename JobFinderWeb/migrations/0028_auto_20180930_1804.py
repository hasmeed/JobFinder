# Generated by Django 2.1 on 2018-09-30 18:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0027_auto_20180927_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
