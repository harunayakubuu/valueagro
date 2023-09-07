from django.contrib import admin
from .models import PrivacyPolicy, Service, TermsAndCondition, Testimonial


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


class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('client', 'created_date', 'public', 'approved')
    # list_editable = ('question', 'answer', 'active')
    list_filter = ('created_date', 'public', 'approved')
    read_only_fields = ['created_date',]
    search_fields = ('client',)

admin.site.register(Testimonial, TestimonialAdmin)
