from django.contrib import admin

from .models import Questions


# Register your models here.


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_question', 'created_time', 'updated_time', 'state']
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
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_content', 'respondent']
