from django.contrib import admin

from frontenduser.models import FrontEndUser


# Register your models here.

@admin.register(FrontEndUser)
class FrontEndUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'short_description', 'django_user', 'head_icon', 'role']


@admin.register(FrontEndUser.RecentBrowsing)
class RecentBrowsingAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'article', 'software', 'browsing_time']
    list_filter = ['user', 'article', 'software', 'browsing_time']
    search_fields = ['user', 'article', 'software', 'browsing_time']
