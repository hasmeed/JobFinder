# Generated by Django 2.1 on 2018-09-16 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0007_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='category',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
