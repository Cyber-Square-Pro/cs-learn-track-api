# Generated by Django 5.1.2 on 2025-01-13 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='active',
            field=models.BooleanField(default=False, verbose_name='Active'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_login',
            field=models.DateTimeField(auto_now=True, verbose_name='Last Login'),
        ),
    ]
