from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm если бы не юзали свою форму
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import Event


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