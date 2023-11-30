from django.contrib import admin

from commentsandposts.models import Comment, Article


# Register your models here.


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'created_time', 'updated_time', 'parent']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'title', 'content', 'created_time', 'updated_time']