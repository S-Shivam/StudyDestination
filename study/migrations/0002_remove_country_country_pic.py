# Generated by Django 3.2.5 on 2021-07-30 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('study', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='country',
            name='country_pic',
        ),
    ]
