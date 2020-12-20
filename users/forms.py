from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserAwards, UserRole, UserPositions, Profile


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
            'team_alias': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'role': forms.Select(attrs={'class': 'form-control'}),
            'characteristic': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'vk_link': forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'})
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', help_text='Длинная пароля не менее 8 символов', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждение пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete': 'off'}))

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