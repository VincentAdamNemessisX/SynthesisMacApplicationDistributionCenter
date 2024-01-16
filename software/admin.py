from django.contrib import admin

from software.models import SoftWare


# Register your models here.
@admin.register(SoftWare)
class SoftWareAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'description', 'link_adrive', 'link_baidu', 'link_123',
                    'link_direct', 'icon', 'status', 'create_date', 'update_date']


@admin.register(SoftWare.SoftwareScreenShots)
class SoftwareScreenShotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'software', 'image']
