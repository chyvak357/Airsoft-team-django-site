from django.db import models
from django.urls import reverse


# TODO подумать, как к меро можно закрепить альбом
class Event(models.Model):
    """Описывает мероприятия команды"""

    def __str__(self):
        return self.name

    name = models.CharField(max_length=128, verbose_name='Название')
    content = models.TextField(verbose_name='Описание мероприятия', blank=True, null=True)
    price = models.IntegerField(verbose_name='Стоимость', blank=True, null=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    is_active = models.BooleanField(default=True, verbose_name='Активно')  # меняется при истечении срока

    location_description = models.CharField(max_length=128, verbose_name='Место проведения', blank=True, null=True)
    location_coord = models.CharField(max_length=128, verbose_name='Координаты', blank=True, null=True)
    meeting_point = models.CharField(max_length=128, verbose_name='Точка сбора', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Добавлено')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')

    close_reg_at = models.DateTimeField(verbose_name='Окончание регистрации', blank=True, null=True)
    starting_at = models.DateTimeField(verbose_name='Начало мероприятия', blank=True, null=True)

    class Meta:
        verbose_name = 'Мероприятие'
        verbose_name_plural = 'Мероприятия'
        ordering = ['-created_at']

    def get_absolute_url(self):
        return reverse('view_events', kwargs={'pk': self.pk})


class UserEvent(models.Model):
    """
    Связывает игрока с мероприятием

    Можно отследить где был и что делал.
    После каждого меро можно дать характеристику конкретно для этого игрока

    0 - пойдёт
    1 - зарегался, но отменил
    # 3 - не пошёл (был зареган, но не пришёл)

     choices=SHIRT_SIZES
    USER_STATUSES = (
        (0, 'Пойдёт'),
        (1, 'Отменил регистрацию'),
        (3, 'Пропустил игру'),
    )
    """
    def __str__(self):
        return self.event.name

    USER_STATUSES = (
        (0, 'Пойдёт'),
        (1, 'Отменил регистрацию'),
        (3, 'Пропустил игру'),
    )
    USER_PAYMENT_STATUS = (
        (False, 'Не оплачено'),
        (True, 'Оплачено'),
    )

    # user будет доступен по свзи MtM
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    user_status = models.IntegerField(default=0, choices=USER_STATUSES, verbose_name='Статус регистрации')
    user_payment = models.BooleanField(default=False, verbose_name='Статус оплаты', choices=USER_PAYMENT_STATUS)
    visited = models.BooleanField(default=False, verbose_name='Посещение')

    user_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий игрока')
    leader_comment = models.TextField(blank=True, null=True, verbose_name='Комментарий пользователя')

    class Meta:
        verbose_name = 'Пользователь-Мероприятие'
        verbose_name_plural = 'Пользователь-Мероприятия'