from django.contrib import admin
from import_export.admin import ExportActionModelAdmin

from frontenduser.models import FrontEndUser


# Register your models here.

@admin.register(FrontEndUser)
class FrontEndUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'state', 'short_description', 'django_user', 'head_icon', 'role']
    search_fields = ['username', 'nickname', 'short_description', 'django_user__username', 'role']
    list_filter = ['role', 'django_user', 'django_user__date_joined']
    ordering = ['django_user__date_joined', 'id']
    list_per_page = 10
    actions = ['ban_user', 'unban_user']

    def ban_user(self, request, queryset):
        for obj in queryset:
            if obj.state == 1:
                continue
            obj.state = 1
            obj.save()
        self.message_user(request, '已封禁！', level='success')

    ban_user.short_description = '封禁'

    def unban_user(self, request, queryset):
        for obj in queryset:
            if obj.state == 2:
                continue
            obj.state = 2
            obj.save()
        self.message_user(request, '已解封！', level='success')

    unban_user.short_description = '解封'


@admin.register(FrontEndUser.RecentBrowsing)
class RecentBrowsingAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'user', 'article', 'software', 'browsing_time']
    list_filter = ['user', 'article', 'software', 'browsing_time']
    search_fields = ['user', 'article', 'software', 'browsing_time']
    ordering = ['-browsing_time', 'id']
    list_per_page = 10
