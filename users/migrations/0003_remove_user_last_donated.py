# Generated by Django 4.2 on 2023-04-27 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_date_joined_remove_user_is_active_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_donated',
        ),
    ]