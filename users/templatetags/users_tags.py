from django import template
from django.db.models import Count, F

from events.models import Event, UserEvent
from users.models import User

register = template.Library()


@register.simple_tag()
def calculate_pbar(reprimand, encouragement):
    """ Вычислени прогресс бара для профиля """
    result = {'reprimand': 0, 'encouragement': 0}

    result['reprimand'] = int((reprimand / (reprimand + encouragement)) * 100)
    result['encouragement'] = int((encouragement / (reprimand + encouragement)) * 100)
    return result