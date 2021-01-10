from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
# from django.contrib.auth.forms import UserCreationForm если бы не юзали свою форму
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import News, Category
from .forms import NewsForm


def index(request):
    return render(request, 'news/index.html', {'page_obj': None})


class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'  # по умолчанию news_list.html
    context_object_name = 'news'  # по умолчанию object_list
    paginate_by = 2  # количетво отображаемых записей на одной странице
    # extra_context = {'title': 'Главная'}  # юзать для статичных данных

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return News.objects.filter(is_published=True).select_related('category')
        else:
            return News.objects.filter(is_published=True, is_public=True).select_related('category')


class NewsByCategory(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')
        else:
            return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True, is_public=True).select_related('category')


# http://127.0.0.1:8000/news/3/

class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'

    def get_object(self, queryset=None):
        obj = super(ViewNews, self).get_object(queryset=queryset)
        if obj.is_public is False and self.request.user.is_authenticated is False:
            print('Пошёл редирект')
            redirect('home')
        else:
            print('Просто вернул обьект')
            return obj


class CreateNews(LoginRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    login_url = '/admin/'  # Куда будет выводить при попытке доступа не авторизованным


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    current_category = Category.objects.get(pk=category_id)
    context = {
        'news': news,
        'title': 'Список новостей: ' + current_category.title,
        'category': current_category
    }
    return render(request, 'news/category.html', context)


def about_page(request):
    return render(request, 'news/about.html')