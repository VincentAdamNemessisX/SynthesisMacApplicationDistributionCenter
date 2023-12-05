from django.contrib import admin

from software.models import SoftWare


# Register your models here.
@admin.register(SoftWare)
class SoftWareAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'description', 'link', 'image', 'date']
