from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserRole, UserPositions, UserAwards


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class UserPositionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'short_description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class UserAwardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


admin.site.register(User, UserAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserPositions, UserPositionsAdmin)
admin.site.register(UserAwards, UserAwardsAdmin)
