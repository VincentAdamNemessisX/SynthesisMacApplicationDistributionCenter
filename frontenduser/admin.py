from django.contrib import admin

from frontenduser.models import FrontEndUser


# Register your models here.

@admin.register(FrontEndUser)
class FrontEndUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'nickname', 'email', 'head_icon', 'role']
