# Generated by Django 5.1.3 on 2024-12-02 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamepark',
            name='image',
        ),
        migrations.AddField(
            model_name='gamepark',
            name='image_1',
            field=models.ImageField(blank=True, null=True, upload_to='gameparks/'),
        ),
        migrations.AddField(
            model_name='gamepark',
            name='image_2',
            field=models.ImageField(blank=True, null=True, upload_to='gameparks/'),
        ),
        migrations.AddField(
            model_name='gamepark',
            name='image_3',
            field=models.ImageField(blank=True, null=True, upload_to='gameparks/'),
        ),
        migrations.AddField(
            model_name='gamepark',
            name='image_4',
            field=models.ImageField(blank=True, null=True, upload_to='gameparks/'),
        ),
        migrations.AddField(
            model_name='gamepark',
            name='image_5',
            field=models.ImageField(blank=True, null=True, upload_to='gameparks/'),
        ),
    ]
