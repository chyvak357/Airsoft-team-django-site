from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout

from .models import UserRole, UserAwards, Profile, UserPositions
from .forms import AwardsForm

def test(request):
    awards = UserAwards.objects.all()
    context = {'awards': awards}
    return render(request, 'users/awards.html', context)


class AwardsList(ListView):
    model = UserAwards
    template_name = 'users/awards.html'
    # template_name = 'users/table_un.html'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        # Для генерации таблицы передаём количество столбцов и для каждоо ширину в процентах
        # context['columns_num'] = 4
        context['columns_data'] = (
            {'col_name': 'id', 'width': 5, 'obj_field': 'pk'},
            {'col_name': 'Название', 'width': 25, 'obj_field': 'name'},
            {'col_name': 'Описание', 'width': 50, 'obj_field': 'description'},
            {'col_name': 'Картинка', 'width': 20, 'obj_field': 'image'}
        )
        return context


class ViewAwards(DetailView):
    model = UserAwards
    template_name = 'users/award_detail.html'


class CreateAwards(CreateView):
    form_class = AwardsForm
    template_name = 'users/add_award.html'
    login_url = '/admin/'




class RolesList(ListView):
    model = UserRole
    template_name = 'users/awards.html'
    allow_empty = False


class ViewRoles(DetailView):
    model = UserRole
    template_name = 'users/award_detail.html'





class PositionsList(ListView):
    model = UserPositions
    template_name = 'users/awards.html'
    allow_empty = False


class ViewPositions(DetailView):
    model = UserPositions
    template_name = 'users/award_detail.html'


# Подходит для получения списка данных
# class AwardsTest(ListView):
#     model = UserAwards
#     allow_empty = False  # Запрет на показ пустых списков. Кинет 404
    # template_name = ''  путьт к шаблону. А так юзает UserAwars_list
    # context_object_name = '' Имя для переменной, а так юзает object_list
    # extra_context = {} Доп данные из context, но не оч использовать его
# Что бы получить данные, то нужно теперь в urls использовать
# AwardsTest.as_view()
#
#     переопределилил метод для добавления данных контекста
#     def get_context_data(self, *, object_list=None, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['titel'] = 'sdasdad'
#         return context

    # Изменяем запрос на получение данных
    # def get_queryset(self):
    #     return UserAwards.objects.filter()


# Так же вызвыается ViewAwards.as_view()
# class ViewAwards(DetailView):
#     model = UserAwards
#     pk_url_kwarg = 'news_id'  # Это что бы хрен искатл не по pk а по news_id как первычный ключ
#     # context_object_name = 'object' по умолчанию


# автоматом будет перехаодить к созданному обьекту
# для этого будет юзать get_absl_url. Иначе кинет ошибку
# class CreateAward(CreateView):
    # form_class = asdasd Указать класс формы
    # template_name = ''
    # success_url = reverse_lazy('home')
