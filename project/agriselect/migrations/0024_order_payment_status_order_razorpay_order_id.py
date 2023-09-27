# Generated by Django 4.2.4 on 2023-09-26 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0023_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('successful', 'Successful'), ('failed', 'Failed')], default='pending', max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='razorpay_order_id',
            field=models.CharField(default=None, max_length=255),
        ),
    ]
