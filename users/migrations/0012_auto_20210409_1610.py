# Generated by Django 3.1.4 on 2021-04-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20210105_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='encouragement',
            field=models.IntegerField(blank=True, default=0, verbose_name='Поощерения'),
        ),
        migrations.AddField(
            model_name='profile',
            name='reprimand',
            field=models.IntegerField(blank=True, default=0, verbose_name='Выговоры'),
        ),
    ]
