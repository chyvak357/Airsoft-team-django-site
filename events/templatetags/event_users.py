from django import template
from django.db.models import Count, F

from events.models import Event, UserEvent
from users.models import User

register = template.Library()

@register.simple_tag()
def get_event_users(event_id):
    # получить все записи пользоветелей, где
    #  среди userEvent есть Event с текущим event_id
    #  И действительной регой

    event_registrations = UserEvent.objects.filter(event_id=event_id, user_status=0)
    users_list = []
    users_list = User.objects.filter(profile__events__in=event_registrations)
    print(users_list)

    return users_list
