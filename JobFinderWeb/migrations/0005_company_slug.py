# Generated by Django 2.1 on 2018-09-15 23:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0004_auto_20180915_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, null=True),
        ),
    ]
