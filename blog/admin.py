from django.contrib import admin
from .models import Category, Activity


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Category, CategoryAdmin)


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = ('active', 'created_at', 'updated_at')
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(Activity, ActivityAdmin)