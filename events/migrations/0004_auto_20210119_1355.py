# Generated by Django 3.1.4 on 2021-01-19 10:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20210119_1353'),
    ]

    operations = [
        migrations.RenameField(
            model_name='event',
            old_name='description',
            new_name='content',
        ),
        migrations.AlterField(
            model_name='event',
            name='close_reg_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Окончание регистрации'),
        ),
        migrations.AlterField(
            model_name='event',
            name='location_description',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Место проведения'),
        ),
        migrations.AlterField(
            model_name='event',
            name='starting_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Начало мероприятия'),
        ),
    ]