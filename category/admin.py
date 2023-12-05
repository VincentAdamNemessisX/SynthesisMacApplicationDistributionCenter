from django.contrib import admin

import category.models


# Register your models here.
@admin.register(category.models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'description']
