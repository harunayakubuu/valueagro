from django.contrib import admin
from .models import Faq


class FaqAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer', 'active', 'created_at', 'updated_at')
    # list_editable = ('question', 'answer', 'is_active')
    list_filter = ('active', 'created_at', 'updated_at')
    read_only_fields = ('created_at', 'updated_at')
    prepopulated_fields = {'slug': ('question',)}
    search_fields = ('question', 'answer')

admin.site.register(Faq, FaqAdmin)