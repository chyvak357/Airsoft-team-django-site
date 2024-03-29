# Generated by Django 3.1.4 on 2021-04-09 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0005_auto_20210206_1923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userevent',
            name='user_payment',
            field=models.BooleanField(choices=[(False, 'Не оплачено'), (True, 'Оплачено')], default=False, verbose_name='Статус оплаты'),
        ),
        migrations.AlterField(
            model_name='userevent',
            name='user_status',
            field=models.IntegerField(choices=[(0, 'Зарегистрировался'), (1, 'Отменил регистрацию'), (2, 'Отказался'), (3, 'Игнорировал'), (4, 'Не явился')], default=0, verbose_name='Статус регистрации'),
        ),
    ]
