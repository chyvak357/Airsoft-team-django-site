# Generated by Django 3.1.4 on 2021-01-19 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userevent',
            options={'verbose_name': 'Пользователь-Мероприятие', 'verbose_name_plural': 'Пользователь-Мероприятия'},
        ),
        migrations.AlterField(
            model_name='event',
            name='close_reg_at',
            field=models.DateTimeField(blank=True, verbose_name='Окончание регистрации'),
        ),
        migrations.AlterField(
            model_name='event',
            name='starting_at',
            field=models.DateTimeField(blank=True, verbose_name='Начало мероприятия'),
        ),
    ]
