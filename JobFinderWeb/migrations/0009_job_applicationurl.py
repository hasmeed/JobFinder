# Generated by Django 2.1 on 2018-09-16 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('JobFinderWeb', '0008_company_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='applicationurl',
            field=models.TextField(blank=True, null=True),
        ),
    ]
