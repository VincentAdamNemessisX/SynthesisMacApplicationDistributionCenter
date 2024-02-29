from django.contrib import admin

from software.models import SoftWare


# Register your models here.
@admin.register(SoftWare)
class SoftWareAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_name', 'version', 'short_description', 'language', 'platform', 'run_os_version',
                    'category', 'tags', 'file_size', 'link_adrive', 'link_baidu', 'link_123', 'link_direct', 'icon', 'state',
                    'created_time', 'updated_time']
    actions = ['pass_audit_batch', 'reject_audit_batch']

    def pass_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.state == 2:
                continue
            obj.state = 2
            obj.save()
        self.message_user(request, '已全部审核通过！', level='success')

    pass_audit_batch.short_description = '审核'

    def reject_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.state == 3:
                continue
            obj.state = 3
            obj.save()
        self.message_user(request, '已全部拒绝！', level='warning')

    reject_audit_batch.short_description = '拒绝'


@admin.register(SoftWare.SoftwareScreenShots)
class SoftwareScreenShotsAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
