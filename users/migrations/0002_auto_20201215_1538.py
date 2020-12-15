# Generated by Django 3.1.4 on 2020-12-15 12:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0002_auto_20201215_1538'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userawards',
            options={'ordering': ['name'], 'verbose_name': 'Награда', 'verbose_name_plural': 'Награды'},
        ),
        migrations.AlterField(
            model_name='user',
            name='awards',
            field=models.ManyToManyField(blank=True, null=True, to='users.UserAwards'),
        ),
        migrations.AlterField(
            model_name='user',
            name='characteristic',
            field=models.TextField(blank=True, null=True, verbose_name='Характеристика'),
        ),
        migrations.AlterField(
            model_name='user',
            name='events',
            field=models.ManyToManyField(blank=True, null=True, related_name='user', to='events.UserEvent'),
        ),
        migrations.AlterField(
            model_name='user',
            name='patronymic',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='Отчество'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='users.userrole', verbose_name='Роль'),
        ),
        migrations.AlterField(
            model_name='user',
            name='team_alias',
            field=models.CharField(blank=True, max_length=64, null=True, unique=True, verbose_name='Позывной'),
        ),
        migrations.AlterField(
            model_name='userawards',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='photos/%Y/%m/%d/', verbose_name='Картинка'),
        ),
        migrations.AlterField(
            model_name='userpositions',
            name='full_description',
            field=models.TextField(blank=True, null=True, verbose_name='Полное описание'),
        ),
        migrations.AlterField(
            model_name='userpositions',
            name='short_description',
            field=models.CharField(blank=True, max_length=512, null=True, verbose_name='Краткое описание'),
        ),
        migrations.AlterField(
            model_name='userrole',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Полное описание'),
        ),
    ]
