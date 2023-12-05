from django.contrib import admin

import announcements.models


# Register your models here.
@admin.register(announcements.models.Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'content', 'date', 'author']
