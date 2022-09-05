# Generated by Django 2.2.16 on 2022-09-04 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='reviews',
            name='unique_review',
        ),
        migrations.AddConstraint(
            model_name='reviews',
            constraint=models.UniqueConstraint(fields=('title_id_id', 'author_id'), name='unique_review'),
        ),
    ]