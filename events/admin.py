from django.contrib import admin
from .models import Event, UserEvent


class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', 'is_published', 'is_active', 'created_at')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name', 'is_published', 'is_active')


class UserEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event', 'user_status', 'user_payment', 'user_comment')
    list_display_links = ('id', 'event')
    search_fields = ('event',)
    list_filter = ('event',)


admin.site.register(Event, EventAdmin)
admin.site.register(UserEvent, UserEventAdmin)
