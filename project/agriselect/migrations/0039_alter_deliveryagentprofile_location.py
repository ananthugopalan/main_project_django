# Generated by Django 5.0.1 on 2024-02-28 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('agriselect', '0038_alter_deliveryagentprofile_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryagentprofile',
            name='location',
            field=models.CharField(choices=[('Ernakulam', 'Ernakulam'), ('Malappuram', 'Malappuram'), ('Pathanamthitta', 'Pathanamthitta'), ('Kannur', 'Kannur')], max_length=100),
        ),
    ]