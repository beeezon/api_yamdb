# Generated by Django 2.2.16 on 2022-08-30 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20220830_2250'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='titles',
            name='rating',
        ),
    ]
