# Generated by Django 5.0.1 on 2024-02-23 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0031_alter_order_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='dispatched',
            field=models.BooleanField(default=False),
        ),
    ]