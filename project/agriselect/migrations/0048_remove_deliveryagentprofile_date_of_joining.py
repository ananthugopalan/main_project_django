# Generated by Django 5.0.1 on 2024-03-05 06:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0047_product_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deliveryagentprofile',
            name='date_of_joining',
        ),
    ]