# Generated by Django 3.2.21 on 2023-09-20 03:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20230919_0730'),
    ]

    operations = [
        migrations.AddField(
            model_name='twofactorauthentication',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 20, 3, 28, 58, 970300)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 27, 3, 27, 58, 562558)),
        ),
    ]