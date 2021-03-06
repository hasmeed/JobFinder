# Generated by Django 2.1 on 2018-09-27 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0026_auto_20180927_0001'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='coverimage',
            field=models.ImageField(blank=True, height_field='height_field', null=True, upload_to='jobcoverimge', width_field='width_field'),
        ),
        migrations.AddField(
            model_name='job',
            name='height_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='width_field',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
