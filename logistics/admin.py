from django.contrib import admin
from . models import Driver, Vehicle, Category, Delivery


class DriverAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'date_of_birth', 'status') 
    search_fields = ('name', 'email') 
    # readonly_fields = ('date_of_birth', )
    list_filter = ('status', ) 
admin.site.register(Driver, DriverAdmin)


class VehicleAdmin(admin.ModelAdmin):
    list_display = ('vehicle_number', 'chasis_number', 'driver', 'status') 
    search_fields = ('vehicle_number', 'chasis_number') 
    list_filter = ('status', ) 
admin.site.register(Vehicle, VehicleAdmin)

admin.site.register(Category)


class DeliveryAdmin(admin.ModelAdmin):
    list_display = ('verhicle', 'pickup_date', 'expected_delivery_date', 'transportation_charges')
    # search_fields = ('vehicle_number', 'chasis_number') 
    # list_filter = ('delivary_status', ) 
admin.site.register(Delivery, DeliveryAdmin)