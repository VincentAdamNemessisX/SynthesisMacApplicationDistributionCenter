from django.contrib import admin

from .models import Questions


# Register your models here.


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id', 'created_time', 'updated_time', 'question_state']


@admin.register(Questions.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'respondent']
