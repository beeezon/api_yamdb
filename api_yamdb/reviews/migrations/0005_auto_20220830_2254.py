# Generated by Django 2.2.16 on 2022-08-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0004_auto_20220830_2254'),
    ]

    operations = [
        migrations.AddField(
            model_name='titles',
            name='rating',
            field=models.PositiveIntegerField(default=None, null=True, verbose_name='Рейтинг'),
        ),
        migrations.AlterField(
            model_name='users',
            name='username',
            field=models.CharField(max_length=50, null=True, unique=True),
        ),
    ]
