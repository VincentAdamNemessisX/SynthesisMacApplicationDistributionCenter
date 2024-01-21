from django.contrib import admin

from software.models import SoftWare


# Register your models here.
@admin.register(SoftWare)
class SoftWareAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'version', 'description', 'language', 'platform', 'run_os_version',
                    'category', 'link_adrive', 'link_baidu', 'link_123', 'link_direct', 'icon', 'state',
                    'create_date', 'update_date']


@admin.register(SoftWare.SoftwareScreenShots)
class SoftwareScreenShotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'software', 'image']
