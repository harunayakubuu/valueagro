from django.contrib import admin
from .models import PrivacyPolicy, Service, TermsAndCondition


class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('policy', 'active', 'created_date', 'updated_date')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('active', 'created_date', 'updated_date')
    read_only_fields = ('created_date', 'updated_date')
    search_fields = ('policy',)

admin.site.register(PrivacyPolicy, PrivacyPolicyAdmin)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'active', 'created_date', 'updated_date')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('active', 'created_date', 'updated_date')
    read_only_fields = ('created_date', 'updated_date')
    search_fields = ('title', 'description')

admin.site.register(Service, ServiceAdmin)


class TermsAndConditionAdmin(admin.ModelAdmin):
    list_display = ('terms_and_conditions', 'active', 'created_date', 'updated_date')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('active', 'created_date', 'updated_date')
    read_only_fields = ('created_date', 'updated_date')
    search_fields = ('term', 'condition')

admin.site.register(TermsAndCondition, TermsAndConditionAdmin)