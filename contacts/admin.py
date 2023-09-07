from django.contrib import admin
from . models import Contact


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'message', 'status', 'created_at', 'updated_at')
    search_fields = ('name', 'email', 'message')
    readonly_fields = ('message', 'created_at', 'updated_at')
    list_filter = ('created_at', 'status')
admin.site.register(Contact, ContactAdmin)