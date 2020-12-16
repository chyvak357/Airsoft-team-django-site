from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserRole, UserPositions, UserAwards, Profile


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


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',
                    'patronymic',
                    'team_alias', 'phone',
                    'birth_date',
                    'position', 'role',
                    'created_at', 'last_online',
                    )
    list_display_links = ('id', 'user')
    search_fields = ('user', 'team_alias')
    list_filter = ('user', 'role', 'position')


# admin.site.register(User, UserAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserPositions, UserPositionsAdmin)
admin.site.register(UserAwards, UserAwardsAdmin)
