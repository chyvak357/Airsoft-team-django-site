from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, reverse, render
from django.views.generic import ListView, DetailView, UpdateView, CreateView
from django.http import HttpResponse
from django.http import HttpResponseRedirect

from .models import Event, UserEvent


# from django.contrib.auth.forms import UserCreationForm если бы не юзали свою форму


class HomeEvents(ListView, LoginRequiredMixin):
    model = Event
    template_name = 'events/events_list.html'
    context_object_name = 'events'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Мероприятия'
        return context

    def get_queryset(self):
        return Event.objects.filter(is_published=True)


class ViewEvents(DetailView):
    """ Для просмотра конкретной игры """

    model = Event
    context_object_name = 'event_item'
    # extra_context = {'latest': Post.objects.all()[:3]}

    def get_object(self, queryset=None):
        obj = super(ViewEvents, self).get_object(queryset=queryset)
        if self.request.user.is_authenticated is False:
            redirect('home')
        else:
            return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user_is_registered'] = False
        context['user_event'] = None
        user_event = self.request.user.profile.events.filter(event=context['object'])
        if user_event.count() != 0 and user_event[0].user_status == 0:
            context['user_is_registered'] = True
            context['user_event'] = user_event[0]
        return context


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
    """ Для регистрации на игру """

    model = UserEvent
    pk = kwargs.get('pk_event')

    obj, created = model.objects.filter(event_id=pk, user=request.user.profile).get_or_create(event_id=pk)

    if created:
        obj.user.add(request.user.profile)
    else:
        # уже был зареган, но отказывался
        obj.user_status = 0
        obj.save()
    return redirect('view_events', pk)


# При отмене регистрации обьект с регистрацией не удаляется, а изменяется статус user_status на 1 (отказался)
def register_cancel(request, *args, **kwargs):
    user_event = UserEvent.objects.get(pk=kwargs.get('pk_reg'))
    user_event.user_status = 1
    user_event.save()
    return redirect('view_events', pk=kwargs.get('pk_event'))

