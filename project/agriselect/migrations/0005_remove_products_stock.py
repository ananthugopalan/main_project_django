# Generated by Django 4.2.4 on 2023-09-06 14:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0004_products_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='stock',
        ),
    ]