# Generated by Django 3.2.21 on 2023-09-24 03:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0015_auto_20230923_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='url',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='twofactorauthentication',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 9, 24, 3, 14, 35, 134363)),
        ),
        migrations.AlterField(
            model_name='usertoken',
            name='expired_at',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 1, 3, 12, 34, 547747)),
        ),
    ]
