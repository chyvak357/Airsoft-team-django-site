# Generated by Django 3.1.4 on 2021-01-02 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
        ('users', '0009_auto_20210102_1559'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='awards',
            field=models.ManyToManyField(blank=True, to='users.UserAwards'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='events',
            field=models.ManyToManyField(blank=True, related_name='user', to='events.UserEvent'),
        ),
    ]
