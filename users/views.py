from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .models import UserRole, UserAwards, Profile, UserPositions
from .forms import AwardsForm, UserRegisterForm, UserEditForm, ProfileEditForm, UserLoginForm
# from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm

# def test(request):
#     awards = UserAwards.objects.all()
#     context = {'awards': awards}
#     return render(request, 'users/awards.html', context)


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
    template_name = 'users/roles.html'
    allow_empty = False


class ViewRoles(DetailView):
    model = UserRole
    template_name = 'users/award_detail.html'



class PositionsList(ListView):
    model = UserPositions
    template_name = 'users/roles.html'
    allow_empty = False


class ViewPositions(DetailView):
    model = UserPositions
    template_name = 'users/award_detail.html'


def register(request):
    if request.method == 'POST':
        profile_form = ProfileEditForm(request.POST)
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save()

            # TODO разобраться, как можно красиво сохранять форму для профиля
            new_user.profile.team_alias = profile_form.cleaned_data['team_alias']
            new_user.profile.phone = profile_form.cleaned_data['phone']
            new_user.profile.role = profile_form.cleaned_data['role']
            new_user.profile.characteristic = profile_form.cleaned_data['characteristic']

            # new_user.profile = profile_form.save()
            new_user.save()
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileEditForm()
    return render(request, 'users/register.html', {'form_u': user_form, 'form_p': profile_form})


# team_alias
# phone
# role
# characteristic
# vk_link

def edit_profile(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Данные успешно изменены')
            return redirect('profile')
        else:
            messages.success(request, 'Ошибка при сохранении данных')
            return redirect('profile')

    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        return render(request, 'users/profile.html', {'form_u': user_form, 'form_p': profile_form})

#
# def edit_profile(request):
#     if request.method == 'POST':
#         user_form = UserEditForm(instance=request.user, data=request.POST)
#         profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
#         if user_form.is_valid() and profile_form.is_valid():
#             user_form.save()
#             profile_form.save()
#             return redirect('home')
#     else:
#         user_form = UserEditForm(instance=request.user)
#         profile_form = ProfileEditForm(instance=request.user.profile)
#         return render(request,
#                       'users/edit.html',
#                       {'user_form': user_form,
#                        'profile_form': profile_form})


# class UsersIO:

# #303030
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('home')


@login_required
def user_profile(request):
    return render(request, 'users/profile.html')



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
