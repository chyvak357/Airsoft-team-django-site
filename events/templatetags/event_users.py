from django import template
from django.db.models import Count, F

from events.models import Event, UserEvent
from users.models import User

register = template.Library()

@register.simple_tag()
def get_event_users(user, event_id):
    """Все пользователи, кто зарегался на игру """
    users_list = []
    event_registrations = UserEvent.objects.filter(event_id=event_id, user_status=0)
    users_list = User.objects.filter(profile__events__in=event_registrations)
    return users_list


@register.simple_tag()
def get_detail_userreg(user, event_id):
    """Доп данные для списка пользователей на игре"""

    # Пример данных: {'id': 21, 'event_id': 6, 'user_status': 0, 'user_payment': False, 'visited': False, 'user_comment': None, 'leader_comment': None}
    test_tmp = UserEvent.objects.get(user__user=user, event_id=event_id)
    return test_tmp


@register.filter(name='cut', is_safe=True)
def cut(value, arg):
    return value.replace(arg, '')