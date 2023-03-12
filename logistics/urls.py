from django.urls import path
from . views import (
    fleet_management,
    vehicle_register,
    vehicle_details,
    vehicle_edit,
    VehicleDeleteView,
    driver_management,
    driver_register, 
    driver_details,
    driver_edit,
    DriverDeleteView,
)

app_name = "logistics"

urlpatterns = [
    path('fleet-management/', fleet_management, name = "fleet-management"),
    path('vehicle/register/', vehicle_register, name = "vehicle-register"),
    path('vehicle/<int:id>/edit/', vehicle_edit, name = "vehicle-edit"),
    path('vehicle/<int:id>/', vehicle_details, name = "vehicle-details"),
    path('vehicle/<int:pk>/delete/', VehicleDeleteView.as_view(), name = 'vehicle-delete'),
    path('driver-management/', driver_management, name = "driver-management"),
    path('driver/register/', driver_register, name = "driver-register"),
    path('driver/<int:id>/edit/', driver_edit, name = "driver-edit"),
    path('driver/<int:id>/', driver_details, name = "driver-details"),
    path('driver/<int:pk>/delete/', DriverDeleteView.as_view(), name = 'driver-delete'),
    
]