# Generated by Django 5.0.1 on 2024-03-05 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0048_remove_deliveryagentprofile_date_of_joining'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='ready_for_pickup',
            field=models.BooleanField(default=False),
        ),
    ]