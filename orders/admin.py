from django.contrib import admin
from .models import Order, OrderItem, OrderDelivery



class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


class OrderDeliveryInline(admin.TabularInline):
    model = OrderDelivery
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['transaction_id', 'user', 'order_status', 'amount', 'created_date', 'updated_date', 'order_session_id']
    # prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['transaction_id', 'user', 'amount', 'created_date', 'updated_date', 'order_session_id']
    search_fields = ['transaction_id', 'created_date', 'updated_date']
    list_filter = ['created_date', 'updated_date']
    
    inlines = [
        OrderItemInline,
        OrderDeliveryInline
    ]
admin.site.register(Order, OrderAdmin)


# admin.site.register(Delivery, DeliveryAdmin)
