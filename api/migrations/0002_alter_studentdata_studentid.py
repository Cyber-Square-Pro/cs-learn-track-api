# Generated by Django 5.1.2 on 2024-10-29 12:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentdata',
            name='studentID',
            field=models.IntegerField(verbose_name='Student Unique Identifier'),
        ),
    ]
