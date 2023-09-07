from django.contrib import admin
from . models import Partner


class PartnerAdmin(admin.ModelAdmin):
    list_display = ('name', 'website', 'active', 'created_date')
    search_fields = ('name',)
    list_filter = ('active',)
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Partner, PartnerAdmin)
