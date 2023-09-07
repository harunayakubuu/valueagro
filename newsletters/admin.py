from django.contrib import admin
from .models import Subscriber, MailMessage


class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed', 'created_at')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('subscribed', 'created_at')
    read_only_fields = ('subscribed', 'created_at',)
    search_fields = ('email',)
admin.site.register(Subscriber, SubscriberAdmin)


class MailMessageAdmin(admin.ModelAdmin):
    list_display = ('title', 'active', 'created_at')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('active', 'created_at',)
    read_only_fields = ('created_at',)
    search_fields = ('title', 'message')
admin.site.register(MailMessage, MailMessageAdmin)