from django.contrib import admin
from import_export.admin import ExportActionModelAdmin
from .models import Questions


# Register your models here.


@admin.register(Questions)
class QuestionsAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'short_question', 'created_time', 'updated_time', 'state']
    search_fields = ['question', 'respondent__username', 'respondent__nickname']
    list_filter = ['state', 'created_time', 'updated_time']
    ordering = ['-created_time', 'id']
    list_per_page = 10
    actions = ['pass_audit_batch']

    def pass_audit_batch(self, request, queryset):
        for obj in queryset:
            if obj.state == 1:
                continue
            obj.state = 1
            obj.save()
        self.message_user(request, '已批量解决！', level='success')

    pass_audit_batch.short_description = '解决'


@admin.register(Questions.Answer)
class AnswerAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'short_content', 'respondent']
    search_fields = ['content', 'respondent__username', 'respondent__nickname']
    list_filter = ['respondent__username']
    ordering = ['-created_time', 'id']
    list_per_page = 10
