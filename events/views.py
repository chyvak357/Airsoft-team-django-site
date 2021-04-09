from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView, View, TemplateView
# from django.http import HttpResponseRedirect
from django.http import HttpResponse

# from django.http import JsonResponse
# from django.core import serializers

import json
from django.core.serializers.json import DjangoJSONEncoder

from .models import Event, UserEvent
from users.models import User


# from django.contrib.auth.forms import UserCreationForm если бы не юзали свою форму


class HomeEvents(ListView, LoginRequiredMixin):
    """ Для просмотра списка игр """

    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мероприятия'
        return context

    def get_queryset(self):
        if 'user-events' in str(self.request):
            # Только те, на которые зареган текущий пользователь

            return Event.objects.filter(pk__in=self.request.user.profile.events.all().values_list('event', flat=True),
                                        userevent__user_status=0, userevent__user=self.request.user.profile)
        return Event.objects.filter(is_published=True)


class ViewEvents(DetailView):
    """ Для просмотра конкретной игры """

    model = Event
    context_object_name = 'event_item'

    def get_object(self, queryset=None):
        obj = super(ViewEvents, self).get_object(queryset=queryset)
        self.set_missed(obj)
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_registered'] = False
        context['user_event'] = None
        context['users_count'] = UserEvent.objects.filter(event=context['object'], user_status=0).count()

        if self.request.user.is_authenticated is False:
            return context

        user_event = self.request.user.profile.events.filter(event=context['object'])
        if user_event.count() != 0:
            context['user_event'] = user_event[0]
        return context

    def set_missed(self, event_obj):
        """ Задать неявку для всех остальных пользователей """
        # 0) Проверить, текущая дата больше даты окончания мероприятия
        # 1) Получить список пользователей, которые не зарегались сюда
        # 2) Пройтись по этому списку и создать для каждого юзер-ивент запись
        # 2.2) Сохранять

        # только те, что уже имеют обьект регистрации на игру
        if event_obj.event_is_over:
            pass

        event_registrations = UserEvent.objects.filter(event=event_obj)
        users_list = User.objects.filter(profile__events__in=event_registrations)

        # TODO вызывает ошибку, тк не поддерживается MySQL
        # truants = User.objects.all().difference(users_list)
        truants = User.objects.all().exclude(id__in=users_list)
        # qs1 = (Local.objects
        #        .values_list('ref')
        #        )
        # qs2 = (Remote.objects
        #        .filter()
        #        .values_list('ref'))
        #
        # qs1.difference(qs1, qs2)

        # check = Qs1.objects.all()
        # prg = []
        # [prg.append(x.ref) for x in check]
        # difference = (Qs2.objects
        #               .exclude(ref__in=prg)
        #               .values()
        #               )

        # check = Qs1.objects.all()
        # prg = []
        # [prg.append(x.ref) for x in check]
        # difference = (Qs2.objects.exclude(ref__in=prg).values())

        #     obj, created = model.objects.filter(event_id=pk, user=request.user.profile).get_or_create(event_id=pk)

        # TODO баг при нескольких вызовах подряд
        user_comment = "Автопрогул. Работа сервера"
        for user in truants:
            # tmp = UserEvent.objects.filter(event=event_obj, user=user.profile)
            # print(tmp)

            tmp, created = UserEvent.objects.filter(user=user.profile).get_or_create(event=event_obj,
                                                                             user_status=3,
                                                                             user_comment=user_comment)
            if created:
                tmp.user.add(user.profile)
            # tmp = UserEvent.objects.create(event=event_obj,
            #                                user_status=3,
            #                                user_comment=user_comment)


# https://coderoad.ru/47939283/django-CBV-generic-DetailView-redirect-%D0%B5%D1%81%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82-%D0%BD%D0%B5-%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82
# class ViewUserEvent(DetailView, LoginRequiredMixin):
#
#     model = UserEvent
#     context_object_name = 'event_item'
#     #     queryset = Publisher.objects.all()
#
#
#     def get_object(self, queryset=None):
#         if self.request.user.is_authenticated is False:
#             return redirect('home')
#
#         pk = self.kwargs.get('pk')
#
#         obj, created = self.model.objects.filter(event_id=pk, user=self.request.user.profile).get_or_create(
#                         event_id=pk
#                     )
#
#         # Если такой уже был, то user_status ставится на 0 (пойдёт)
#         if created:
#             obj.user.add(self.request.user.profile)
#         return obj


def register_event(request, *args, **kwargs):
    """ Для регистрации на игру

        USER_STATUSES = (
        (0, 'Зарегистрировался'),
        (1, 'Отменил регистрацию'),  # Ранее да, но потом отказался. Указал причину
        (2, 'Отказался'),            # С указанием причины
        (3, 'Игнорировал'),          # Ставится по умолчанию для тех, кто не голосовал после завершения меро
        (4, 'Не явился'),            # Зареган, но не приехал. Проставляется командиром
    )
    """
    model = UserEvent
    user_comment = None

    if request.method == 'POST':
        try:
            user_comment = json.loads(request.body).get('user_comment', None)
        except Exception as err:
            user_comment = 'Server side error'

    pk = kwargs.get('pk_event')
    obj, created = model.objects.filter(event_id=pk, user=request.user.profile).get_or_create(event_id=pk)

    if created:
        obj.user.add(request.user.profile)
        obj.user_status = 2 if request.method == 'POST' else 0
        obj.user_comment = user_comment
        obj.save()
    else:
        # Сначала отказался, а потом передумал
        obj.user_status = 2 if request.method == 'POST' else 0
        obj.user_comment = user_comment
        obj.save()
    return redirect('view_events', pk)


# При отмене регистрации обьект с регистрацией не удаляется, а изменяется статус user_status на 1 или 2 (отказался)
@login_required
def register_cancel_visit(request, *args, **kwargs):
    """ Отмена/изменение регистрации на игру
        pk_event ключ на событие, а в get параметрах передать id регистрации
    """
    response = {'stateside': 200}

    pk_reg = request.GET.get('reg_id', None)
    if pk_reg:
        user_event = UserEvent.objects.get(pk=pk_reg)
        if user_event.user_status == 0:
            user_event.user_status = 4  # неявился
            user_event.visited = False
            user_event.user_comment = 'Неявка. Командир группы'
            user_event.save()
        else:
            user_event.user_status = 0  # зарегистрировался
            user_event.visited = True
            user_event.user_comment = ''
            user_event.save()
    return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json')


# Подходит для получения списка данных
# class EventUsersList(ListView):
#     """ Таблица с теми, кто зарегался на игру"""
#     model = UserEvent
#     allow_empty = False  # кинет 404 при попытке отобразить пустой список
#     template_name = 'events/users_on_event_static.html'
#     extra_context = {}
# #     Доп данные из context, но не оч использовать его
# # Что бы получить данные, то нужно теперь в urls использовать
# # AwardsTest.as_view()
#
#     # Изменяем запрос на получение данных
#     def get_queryset(self):
#         pk = self.kwargs.get('pk')
#         # Номер текущей игры
#         users_list = []
#
#         event_registrations = UserEvent.objects.filter(event_id=pk, user_status=0)
#         users_list = User.objects.filter(profile__events__in=event_registrations)
#         return users_list
#
#     # переопределилил метод для добавления данных контекста
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['title'] = 'Просто пример чего-то там'
#         context['event_pk'] = self.kwargs.get('pk')
#         return context

# http://127.0.0.1:8000/events/event/5/user-table?cancel_table=true

class EventUsersList(View):
    """ Таблица пользователей связанных с мероприятием"""

    context = {}
    template_name = 'events/users_on_event.html'
    extra_template_name = 'events/users_on_event_check.html'
    cancel_table = False

    def get(self, request, *args, **kwargs):
        # ожидаемый параметр, для открытия таблицы с возможностью подтверждать регистрацию
        template_name = self.template_name if not request.GET.get('cancel_table', None) else self.extra_template_name
        self.context['title'] = 'Список участников'
        self.context['event_pk'] = self.kwargs.get('pk')
        return render(request, template_name, self.context)



class EventUsersListTest(LoginRequiredMixin, View):
    """ Контролер для полоучения табличных данных формата json
        работает со списком заререстрировавшихся на игру пользователей
    """
    model = UserEvent
    user_statuses = dict((k, v) for k, v in model.USER_STATUSES)

    def get(self, request, pk):
        response = {}
        # pk - индекс мероприятия
        # data = self.model.objects.filter(event_id=pk)
        # user = auth.get_user(request)

        request_filter = request.GET.get('filter_patt', None)  # будет набор заготовленных фильтров
        # cancelTable - только те, что отметились, что едут на игру

        user_groups = request.user.groups.values_list('name', flat=True)
        is_leader = 'GroupLeaders' in user_groups

        qs_filter = {'event_id': pk}

        if request_filter == 'cancelTable':
            qs_filter['user_status__in'] = [0, 4]

        # Для обычных бойцов показывать только тех, кто едет на игру
        if not is_leader:
            qs_filter['user_status'] = 0

        data = list(self.model.objects.filter(**qs_filter).values('pk', 'user_status', 'user_comment', 'visited',
                                                                  'user__user', 'user__team_alias',
                                                                  'user__user__first_name', 'user__user__last_name',
                                                                  ))

        for row in data:
            # if not is_leader and row['user_status'] != 0:
            #     continue
            row['user_name'] = '{} {}'.format(row['user__user__last_name'], row[
                'user__user__first_name'])  # qs_json = serializers.serialize('json', data)  # нельзя использовать, есл указывать какие поля нужно получить
            row['user_pk'] = row.pop('user__user')
            row['user_event_pk'] = row.pop('pk')
            row['user_status_code'] = row['user_status']
            row['user_status'] = self.user_statuses.get(row['user_status'], 'Error')
            row['user_team_alias'] = row['user__team_alias']

            row.pop('user__team_alias')
            row.pop('user__user__first_name')
            row.pop('user__user__last_name')

        response['Data'] = data
        response['Columns'] = [
            {'name': 'user_name',
             'displayName': 'Пользователь',
             'search': 1,
             'sort': 1,
             'width': ''
             },
            {'name': 'user_team_alias',
             'displayName': 'Позывной',
             'search': 1,
             'sort': 1,
             'width': ''

             },
            {'name': 'user_status',
             'displayName': 'Статус регистрации',
             'search': 0,
             'sort': 1,
             'width': ''
             }
        ]

        # Для лидера группы показывать статус регистрации игрока и его комент
        if is_leader and not request_filter == 'cancelTable':
            response['Columns'].append(
                {'name': 'user_comment',
                 'displayName': 'Комментарий пользователя',
                 'search': 0,
                 'sort': 0,
                 'width': ''
                 }
            )

        return HttpResponse(json.dumps(response, cls=DjangoJSONEncoder), content_type='application/json')

# def test(request):
#     return render(request, 'events/test_table_copy.html', {})
