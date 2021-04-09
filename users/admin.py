from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import UserRole, UserPositions, UserAwards, Profile


class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class UserPositionsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)


class UserAwardsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    list_filter = ('name',)



class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'display_username',
                    'team_alias', 'division','phone',
                    'birth_date',
                    'position', 'role',
                    'vk_link',
                    # 'last_online',
                    )
    list_display_links = ('id', 'user', 'team_alias')
    search_fields = ('user', 'team_alias', 'division')
    list_filter = ('user', 'role', 'position', 'division')
    list_editable = ('division',)

    def display_username(self, obj):
        name = 'ERROR'
        try:
            name = f'{obj.user.last_name} {obj.user.first_name}'
        except Exception:
            pass
        return name



admin.site.register(Profile, ProfileAdmin)
admin.site.register(UserRole, UserRoleAdmin)
admin.site.register(UserPositions, UserPositionsAdmin)
admin.site.register(UserAwards, UserAwardsAdmin)
