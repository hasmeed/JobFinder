# Generated by Django 2.1 on 2018-09-23 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0018_resumee_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumee',
            name='status',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
    ]
