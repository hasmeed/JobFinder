# Generated by Django 2.1 on 2018-09-21 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0016_auto_20180920_2157'),
    ]

    operations = [
        migrations.AlterField(
            model_name='education',
            name='datefrom',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='dateto',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
