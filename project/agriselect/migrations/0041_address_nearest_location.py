# Generated by Django 5.0.1 on 2024-03-04 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0040_deliveryagentprofile_date_of_birth_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='nearest_location',
            field=models.CharField(blank=True, choices=[('Ernakulam', 'Ernakulam'), ('Malappuram', 'Malappuram'), ('Pathanamthitta', 'Pathanamthitta'), ('Kannur', 'Kannur')], max_length=100, null=True),
        ),
    ]