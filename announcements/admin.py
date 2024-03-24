from django.contrib import admin
from import_export.admin import ExportActionModelAdmin

import announcements.models


# Register your models here.
@admin.register(announcements.models.Announcements)
class AnnouncementsAdmin(ExportActionModelAdmin, admin.ModelAdmin):
    list_display = ['id', 'short_title', 'short_content', 'created_time', 'author']
    search_fields = ['title', 'content', 'author__username', 'author__nickname']
    ordering = ['-created_time', 'id']
    list_filter = ['author', 'created_time']
    list_per_page = 10
