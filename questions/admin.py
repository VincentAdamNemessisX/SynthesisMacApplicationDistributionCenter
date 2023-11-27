from django.contrib import admin

from questions.models import Questions


# Register your models here.


@admin.register(Questions)
class QuestionsAdmin(admin.ModelAdmin):
    list_display = ['id']
