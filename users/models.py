from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, BaseUserManager



class UserPositions(models.Model):
    """
    Должности внутри команды

    Командир, зам. командира, зав. Имуществом и т.д.
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=64, verbose_name='Должность', unique=True)
    short_description = models.CharField(max_length=512, verbose_name='Краткое описание', blank=True, null=True)
    full_description = models.TextField(verbose_name='Полное описание', blank=True, null=True)

    class Meta:
        verbose_name = 'Должность'
        verbose_name_plural = 'Должности'
        ordering = ['name']


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


class UserAwards(models.Model):
    """
    Награды и знаки отличия

    Многим-ко-многим с User
    """

    def __str__(self):
        return self.name

    name = models.CharField(max_length=64, verbose_name='Роль', unique=True)
    description = models.TextField(verbose_name='Полное описание')
    image = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Картинка', blank=True, null=True)

    class Meta:
        verbose_name = 'Награда'
        verbose_name_plural = 'Награды'
        ordering = ['name']


# class UserManager(BaseUserManager):
#
#     use_in_migrations = True
#
#     def _create_user(self, username, password, **extra_fields):
#         """Create and save a User with the given email and password."""
#         user = self.model(username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password=None, **extra_fields):
#         """Create and save a regular User with the given email and password."""
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         """Create and save a SuperUser with the given email and password."""
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Переопределённая модель для пользователя

    Многим-ко-многим (MtM)с UserAwards
    https://docs.djangoproject.com/en/3.1/topics/db/examples/many_to_many/

    MtO UserRole
    MtO UserPositions
    """

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    # login == username
    # first_name
    # last_name
    # email
    patronymic = models.CharField(max_length=32, blank=True, null=True, verbose_name='Отчество')
    team_alias = models.CharField(max_length=64, blank=True, null=True, verbose_name='Позывной', unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона', unique=True)
    birth_date = models.DateField(null=True, blank=True)

    # TODO проверить работу поля position
    position = models.ForeignKey(UserPositions, on_delete=models.PROTECT, verbose_name='Должность', blank=True)

    # TODO проверить работу поля role
    role = models.ForeignKey(UserRole, on_delete=models.PROTECT, verbose_name='Роль', null=True, blank=True)
    characteristic = models.TextField(blank=True, null=True, verbose_name='Характеристика')

    # TODO проверить работу поля awards
    awards = models.ManyToManyField(UserAwards, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлен', null=True)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d/', verbose_name='Фото', null=True, blank=True)

    last_online = models.DateTimeField(blank=True, null=True)

    # TODO проверить работу поля events
    events = models.ManyToManyField('events.UserEvent', null=True, blank=True, related_name='user')

    # objects = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    # def get_absolute_url(self):
    #     return reverse('users:profile', kwargs={'user': self.username})
    #
    # def initials(self):
    #     return get_initials(self)

# test_user1 = User.objects.create(username='test_user',
#                                  first_name='Test_n',
#                                  last_name='Test_ln',
#                                  patronymic='Test_pat',
#                                  email='test@mail.ru',
#                                  team_alias='test_alias1',
#                                  phone='8800555353')