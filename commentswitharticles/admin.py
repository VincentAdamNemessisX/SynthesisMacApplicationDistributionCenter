from django.contrib import admin

from commentswitharticles.models import Comment, Article


# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'correlation_article', 'correlation_software',
                    'state', 'created_time', 'parent']
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


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'content', 'correlation_software', 'state', 'created_time',
                    'updated_time']
