from django.contrib import admin
from . models import ProcurementRequest, ProcurementItem


class ProcurementItemInline(admin.TabularInline):
    model = ProcurementItem
    fields = ('item_name', 'unit_price', 'quantity_needed', 'total_price', 'reason_for_item_need')
    extra = 1
    

class ProcurementRequestAdmin(admin.ModelAdmin):
    list_display = ['title', 'md_approval_status', 'chairman_approval_status']
    list_filter = ['md_approval_status', 'chairman_approval_status']
    inlines = [
        ProcurementItemInline,
    ]

admin.site.register(ProcurementRequest, ProcurementRequestAdmin)