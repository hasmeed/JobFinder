# Generated by Django 2.1 on 2018-09-26 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0022_auto_20180926_0558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='height_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='width_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
