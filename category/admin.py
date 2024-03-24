from django.contrib import admin

import category.models


# Register your models here.
@admin.register(category.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'short_name', 'slug', 'icon', 'short_description']
    search_fields = ['name', 'slug', 'short_description']
    ordering = ['name', 'id']
    list_per_page = 10
