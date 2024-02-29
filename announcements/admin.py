from django.contrib import admin

import announcements.models


# Register your models here.
@admin.register(announcements.models.Announcements)
class AnnouncementsAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_title', 'short_content', 'created_time', 'author']
    search_fields = ['title', 'content', 'author__username', 'author__nickname']
