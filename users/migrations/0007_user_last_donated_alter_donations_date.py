# Generated by Django 4.2 on 2023-04-27 15:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_area'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_donated',
            field=models.DateField(default=datetime.date(1997, 10, 19), null=True),
        ),
        migrations.AlterField(
            model_name='donations',
            name='date',
            field=models.DateField(default=datetime.date(1997, 10, 19), null=True),
        ),
    ]