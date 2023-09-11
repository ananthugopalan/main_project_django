# Generated by Django 4.2.4 on 2023-09-06 15:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('agriselect', '0005_remove_products_stock'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='products',
            name='price',
        ),
        migrations.CreateModel(
            name='SeedProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('weight_option_100gm', models.BooleanField(blank=True, null=True)),
                ('price_100gm', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('weight_option_150gm', models.BooleanField(blank=True, null=True)),
                ('price_150gm', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('product_image', models.ImageField(upload_to='seed_product_images/')),
                ('seller', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CropProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('product_category', models.CharField(max_length=100)),
                ('product_subcategory', models.CharField(max_length=100)),
                ('product_image', models.ImageField(upload_to='crop_product_images/')),
                ('seller', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]