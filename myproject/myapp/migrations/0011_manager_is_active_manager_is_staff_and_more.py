# Generated by Django 5.1.3 on 2024-12-08 07:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_manager_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='manager',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='manager',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='manager',
            name='last_login',
            field=models.DateTimeField(blank=True, null=True, verbose_name='last login'),
        ),
        migrations.AlterField(
            model_name='manager',
            name='password',
            field=models.CharField(max_length=128, verbose_name='password'),
        ),
    ]
