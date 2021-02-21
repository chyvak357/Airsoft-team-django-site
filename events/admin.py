from django.contrib import admin
from .models import Event, UserEvent
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django import forms


class EventAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Event
#         created_at
#         updated_at
#         close_reg_at
#         starting_at
        fields = '__all__'


class EventAdmin(admin.ModelAdmin):
    form = EventAdminForm
    list_display = ('id', 'name', 'price', 'is_published', 'is_active', 'created_at', 'starting_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', 'is_published', 'is_active')
    list_editable = ('price', 'is_published', 'is_active', 'starting_at')


class UserEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'display_user_name', 'event', 'user_status', 'user_payment', 'user_comment')

    list_display_links = ('id', 'event')
    search_fields = ('event__name', )
    list_filter = ('event__name', 'user_status', 'user_payment')

    def display_user_name(self, obj):
        user_prof = obj.user.all()[0]
        return f'{user_prof.user.last_name} {user_prof.user.first_name}'


admin.site.register(Event, EventAdmin)
admin.site.register(UserEvent, UserEventAdmin)
