# Generated by Django 5.0 on 2024-03-20 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0054_order_verified'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliveryagentprofile',
            name='pincode',
            field=models.CharField(default='Null', max_length=6),
        ),
    ]