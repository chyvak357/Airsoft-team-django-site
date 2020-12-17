from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import UserAwards, UserRole, UserPositions


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