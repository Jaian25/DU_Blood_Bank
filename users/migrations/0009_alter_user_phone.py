# Generated by Django 4.2 on 2023-04-27 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_user_number_of_donations_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=64, null=True, unique=True),
        ),
    ]
