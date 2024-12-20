# Generated by Django 5.1.4 on 2024-12-05 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_booking'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='booking_images/'),
        ),
        migrations.AddField(
            model_name='booking',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='booking',
            name='transport',
            field=models.CharField(blank=True, choices=[('bus', 'Bus'), ('car', 'Car'), ('bike', 'Bike'), ('walk', 'Walk')], max_length=50, null=True),
        ),
    ]
