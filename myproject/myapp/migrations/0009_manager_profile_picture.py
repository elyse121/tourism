# Generated by Django 5.1.3 on 2024-12-07 21:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_booking_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile_pics/'),
        ),
    ]
