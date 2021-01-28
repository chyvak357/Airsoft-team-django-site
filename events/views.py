from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm если бы не юзали свою форму
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import Event, UserEvent


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
    model = Event
    context_object_name = 'event_item'

    def get_object(self, queryset=None):
        obj = super(ViewEvents, self).get_object(queryset=queryset)

        if self.request.user.is_authenticated is False:
            redirect('home')
        else:
            return obj


# https://coderoad.ru/47939283/django-CBV-generic-DetailView-redirect-%D0%B5%D1%81%D0%BB%D0%B8-%D0%BE%D0%B1%D1%8A%D0%B5%D0%BA%D1%82-%D0%BD%D0%B5-%D1%81%D1%83%D1%89%D0%B5%D1%81%D1%82%D0%B2%D1%83%D0%B5%D1%82
class ViewUserEvent(DetailView):

    model = UserEvent
    context_object_name = 'event_item'

    def get_object(self, queryset=None):
        print(123)
        obj = super(ViewUserEvent, self).get_object(queryset=queryset)
        print(456)
        if obj is None:
            print('is None')
        if self.request.user.is_authenticated is False:
            redirect('home')
        else:
            return obj