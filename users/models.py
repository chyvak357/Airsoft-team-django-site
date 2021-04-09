from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



class UserPositions(models.Model):
    """
    Должности внутри команды

    Командир, зам. командира, зав. Имуществом и т.д.
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=64, verbose_name='Должность', unique=True)
    description = models.CharField(max_length=512, verbose_name='Краткое описание', blank=True, null=True)
    full_description = models.TextField(verbose_name='Полное описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('positions_detail', kwargs={'pk': self.pk})


class UserRole(models.Model):
    """
    Роль/звание в составе группы

    Рекрут, Стрелок, ст. Стрелок. Военврач, стрелок-пулемётчик, Стрелок-Снайпер
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=64, verbose_name='Роль', unique=True)
    description = models.TextField(verbose_name='Полное описание', blank=True, null=True,)

    class Meta:
        verbose_name = 'Роль'
        verbose_name_plural = 'Роли'
        ordering = ['name']

    def get_absolute_url(self):
        return reverse('roles_detail', kwargs={'pk': self.pk})


class UserAwards(models.Model):
    """
    Награды и знаки отличия

    Многим-ко-многим с User
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=64, verbose_name='Награда', unique=True)
    description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(upload_to='awards_pic/%Y/%m/%d/', verbose_name='Картинка', null=True, blank=True)

    class Meta:
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'
        # ordering = ['name']

    def get_absolute_url(self):
        return reverse('awards_detail', kwargs={'pk': self.pk})


# TODO Можно добавить поле с описанием от игрока. Типа "О себе"
class Profile(models.Model):
    """
    Дополнительная модель для пользователя

    OtO с User

    Многим-ко-многим (MtM)с UserAwards
    https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/

    MtO UserRole
    MtO UserPositions
    """

    def __str__(self):
        # return f'{self.user.last_name} {self.user.first_name}'
        return f'Профиль_пользователя {self.user.username}'

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # login == username
    # first_name
    # last_name
    # email
    team_alias = models.CharField(max_length=64, blank=True, null=True, verbose_name='Позывной', unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона', unique=True)
    vk_link = models.CharField(max_length=64, blank=True, null=True, verbose_name='Ссылка ВК')
    # TODO разобраться с формой для дня рождения
    birth_date = models.DateField(null=True, blank=True)

    position = models.ForeignKey(UserPositions, on_delete=models.PROTECT, verbose_name='Должность', blank=True, null=True)

    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, verbose_name='Роль', null=True, blank=True)
    characteristic = models.TextField(blank=True, null=True, verbose_name='Характеристика')

    awards = models.ManyToManyField(UserAwards, blank=True)

    reprimand = models.IntegerField(blank=True, default=0, verbose_name='Выговоры')
    encouragement = models.IntegerField(blank=True, default=0, verbose_name='Поощерения')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен', null=True, blank=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d/', verbose_name='Фото', null=True, blank=True)

    # last_online = models.DateTimeField(blank=True, null=True)

    events = models.ManyToManyField('events.UserEvent', blank=True, related_name='user')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        # ordering = ['user.username']

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()


# test_user1 = User.objects.create(username='test_user',
#                                  first_name='Test_n',
#                                  last_name='Test_ln',
#                                  patronymic='Test_pat',
#                                  email='test@mail.ru',
#                                  team_alias='test_alias1',
#                                  phone='8800555353')