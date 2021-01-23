# from django import forms
# from django.core.exceptions import ValidationError
#
# from .models import Event
#
#
# class EventForm(forms.ModelForm):
#     class Meta:
#         model = Event
#         # fields = '__all__' использование всех полей
#         fields = ['name',
#                   'description',
#                   'is_published',
#                   'is_active',
#                   'price',
#                   'location_description',
#                   'location_coord',
#                   'meeting_point',
#                   'starting_at',
#                   'close_reg_at'
#                   ]
#
#         # widgets = {
#         #     'title': forms.TextInput(attrs={'class': 'form-control'}),
#         #     'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
#         #     'category': forms.Select(attrs={'class': 'form-control'})
#         # }