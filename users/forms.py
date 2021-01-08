from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserAwards, UserRole, UserPositions, Profile

import re

# TODO не загружает картинки из формы. Из Админки работает
class AwardsForm(forms.ModelForm):
    class Meta:
        model = UserAwards
        fields = '__all__'
        # fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            # 'image': forms.ImageField()
        }


class RoleForm(forms.ModelForm):
    class Meta:
        model = UserRole
        fields = '__all__'
        # fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class PositionsForm(forms.ModelForm):
    class Meta:
        model = UserPositions
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
        }


class UserEditForm(UserChangeForm):
    """Для встроенной пользовательской модели"""
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.Select(attrs={'class': 'form-control'})
        }


# TODO Добавить валидацию и проверку уникальности для полей
class ProfileEditForm(forms.ModelForm):
    """Для профиля"""
    class Meta:
        model = Profile
        # fields = ('patronymic', 'team_alias', 'phone', 'birth_date', 'position', 'role'
        fields = ['team_alias', 'phone', 'role', 'characteristic', 'vk_link']
        widgets = {
            'team_alias': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Твой позывной, боец!?'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '8 800 555 3535'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'characteristic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'autocomplete': 'off', 'placeholder': 'Коротко о себе'}),
            'vk_link': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'vk.com/...'})
        }

    def clean_vk_link(self):
        link = self.cleaned_data['vk_link']
        if link is None:
            return None
        result = re.match(r'''(http[s]?://)?(vk\.com)([\/\w \.-]*)*\/?$''', link)
        if result:
            if not result.group(1):
                link = 'https://' + link
            return link
        else:
            raise ValidationError('Ссылка должна соотвествоать формату vk.com/[example или id888000]')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        result = re.match(r'''^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$''', phone)
        if result:
            phone = phone.replace(' ', '')
            phone = phone.replace('-', '')
            phone = phone.replace('(', '')
            phone = phone.replace(')', '')
            return phone
        else:
            raise ValidationError('Номер должен соотвествовать формату 88005553535')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'login'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'password'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'}))
    password1 = forms.CharField(label='Пароль', help_text='Длинная пароля не менее 8 символов', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off', 'placeholder': 'Фамилия'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')
        # widgets = {
        #     'username': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
        #     'password2': forms.PasswordInput(attrs={'class': 'form-control'})
        # }




# class UserRegProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         # fields = '__all__' использование всех полей
#         fields = [
#             'patronymic',
#             'team_alias',
#             'phone',
#             'birth_date',
#             # 'position',
#             'role'
#         ]
#         widgets = {
#             'patronymic': forms.TextInput(attrs={'class': 'form-control'}),
#             'team_alias': forms.TextInput(attrs={'class': 'form-control'}),
#             'phone': forms.TextInput(attrs={'class': 'form-control'}),
#             'birth_date': forms.DateInput(format='%d %b %Y'),
#             # 'position': forms.Select(attrs={'class': 'form-control'}),
#             'role': forms.Select(attrs={'class': 'form-control'})

            # 'title': forms.TextInput(attrs={'class': 'form-control'}),
            # 'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            # 'category': forms.Select(attrs={'class': 'form-control'})
        # }

    # валидатор для формы clean_*
    # def clean_title(self):
    #     title = self.cleaned_data['title']
    #     if re.match(r'\d', title):
    #         raise ValidationError('Название не должно начинаться с цифры')
    #     return title