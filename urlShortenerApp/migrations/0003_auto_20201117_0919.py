# Generated by Django 3.1.3 on 2020-11-17 09:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('urlShortenerApp', '0002_auto_20201117_0855'),
    ]

    operations = [
        migrations.AddField(
            model_name='analyticslist',
            name='city',
            field=models.TextField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='analyticslist',
            name='country',
            field=models.TextField(max_length=50, null=True),
        ),
    ]
