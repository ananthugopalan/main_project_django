# Generated by Django 4.2.4 on 2023-08-30 13:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0004_customuser_username'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]
