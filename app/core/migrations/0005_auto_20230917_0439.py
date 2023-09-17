# Generated by Django 3.2.21 on 2023-09-17 04:39

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_auto_20230917_0409'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='phonenumber',
            field=models.CharField(max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 4, 39, 50, 306396)),
        ),
    ]
